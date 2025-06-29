#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import pathlib
import matplotlib.pyplot as plt
import sys
sys.path.append('ext')
import plot_util
import accelerometers

smooth_before_plot=100
smooth_when_plot=1

inputdir = pathlib.Path.cwd() / 'inputdata'

outputdir = pathlib.Path.cwd() / 'outputdata'
outputdir.mkdir(exist_ok=True)

print(pathlib.Path.cwd())

# Adapt paths if needed.
# I use two layers of sub-directories to link to an icloud directory with sub-directories named based on trip category.

files = list(inputdir.glob('*/*/Accelerometer.csv'))
{i: files[i] for i in np.arange(len(files))}

ps_collection = {} # Save for subsequent plots
tot_pow_collection = {}
g_collection = {}

for file in files:
    df = accelerometers.clean_file(file)

    title = str(file.parents[1].stem) + accelerometers.DELIMITTER + str(file.parent.stem)
    print('\n', title)

    # Norm over time, in units of g-force
    if not pathlib.Path(outputdir / (title + '_gforce.png')).exists():
        plt.figure()
        plot_util.generic_plot(accelerometers.smooth(df[['g-force']], smooth_before_plot), kind='line', xlabel='Sec Elapsed', ylabel='g',
                               title=title + '_gforce', output_directory=outputdir)
        plt.close()
    ps = accelerometers.ps(df, smooth_window=smooth_before_plot) # Slight smooth before plotting, as will be later interpolated

    # Save for later
    ps_collection[title] = ps.copy()

    # Log power spectrum, logged x
    if not pathlib.Path(outputdir / (title + '_logx.png')).exists():
        ps_smoothed = accelerometers.smooth(ps, smooth_window=smooth_when_plot)
        plt.figure()
        plot_util.generic_plot(np.log10(ps_smoothed[accelerometers.POWER_LABEL]).rename(np.log10, axis=0), kind='line', xlabel='Hz', ylabel='g$^2$/Hz', logy=True, logx=True,
                               title=title + '_logx', output_directory=outputdir)
        plt.close()

    total_pow = np.trapezoid(ps[accelerometers.POWER_LABEL], x=ps.index)
    tot_pow_collection[title] = total_pow
    g_collection[title] = df['g-force'].mean()

    print('Total Power (variance of acceleration): ' + str(round(total_pow, 4)) + ' g^2')
    print('Mean g-force: ' + str(df['g-force'].mean().round(2)) + " g's")

print(len(ps_collection))

combined = accelerometers.interp_combine(ps_collection)

combined.to_csv(outputdir / 'Combined.csv')

agg_stats_df = pd.DataFrame(index=['Power [g^2]', 'g-force [-]'], columns=combined.columns)
idx = pd.IndexSlice
for col in combined:
    agg_stats_df.loc[idx['Power [g^2]'], idx[col[0], col[1]]] = tot_pow_collection[col[0] + accelerometers.DELIMITTER + col[1]]
    agg_stats_df.loc[idx['g-force [-]'], idx[col[0], col[1]]] = g_collection[col[0] + accelerometers.DELIMITTER + col[1]]
print(agg_stats_df.T)

agg_stats_df.to_csv(outputdir / 'Aggregate Stats by Trip.csv')

# Print number of trips by category
print('Number of Trips')
print(combined.groupby('Category', axis=1).count().T[combined.index[0]])

# Take the log before the average to avoid domination of occasional noise
# Equivalent to geometric rather than arithmetic mean
# Smooth after averaging
combined_bycat_log = accelerometers.smooth(combined.map(np.log10).groupby('Category', axis=1).mean(), smooth_when_plot)
plot_util.generic_plot(combined_bycat_log.rename(np.log10, axis=0), kind='line', xlabel='Hz', ylabel='g$^2$/Hz',
                       output_directory=outputdir, title='Average Power Spectra by Mode', logx=True, logy=True)

grouped_stats = agg_stats_df.T.groupby(level=0).mean()
grouped_stats.to_csv(outputdir / 'Grouped Aggregated Stats by Trip.csv')
print(grouped_stats)

print('Standard Errors')
z_grouped_stats = (agg_stats_df.T.groupby(level=0).std() / agg_stats_df.T.groupby(level=0).mean()).map(lambda x: np.round(x, 2))
z_grouped_stats.to_csv(outputdir / 'Z for Grouped Agg Stats by Trip.csv')
print(z_grouped_stats)

# Summary chart: rms acceleration
pow_seg = accelerometers.pow_range(combined_bycat_log)
plot_util.generic_plot(pow_seg.map(np.sqrt).T, kind='bar', ylabel='g', unstacked=True, title='RMS Acceleration by Freq. Range & Mode',
                       output_directory=outputdir, fontsize=7)

# Summarize by mode type
# Currently used types of modes
mode_types = list(set([accelerometers.mode_map(mode) for mode in combined_bycat_log.columns]))

for t in mode_types:
    modes = accelerometers.mode_match(combined_bycat_log.columns, t)

    # Separate chart for each type of mode
    plot_util.generic_plot(combined_bycat_log[modes].rename(np.log10, axis=0), kind='line',
                           xlabel='Hz', ylabel='g$^2$/Hz', output_directory=outputdir,
                           title='Average Power Spectra for ' + t + ' Travel Modes', logx=True, logy=True)

    plot_util.generic_plot(pow_seg[modes].T, kind='bar', ylabel='g$^2$', title='Power by Freq. Range for ' + t + ' Modes',
                           output_directory=outputdir)

# Average over mode type
combined_bymode_type = combined_bycat_log.rename(accelerometers.mode_map, axis=1).groupby('Category', axis=1).mean()
plot_util.generic_plot(combined_bymode_type.rename(np.log10, axis=0), kind='line', xlabel='Hz', ylabel='g$^2$/Hz',
                       output_directory=outputdir, title='Average Power Spectra by Mode Type',
                       logx=True, logy=True)

print('% of Power')
print(pow_seg / pow_seg.sum())
pow_seg.T.to_csv(outputdir / 'Power by Freq. Range.csv')

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

    # Log power spectrum
    if not pathlib.Path(outputdir / (title + '.png')).exists():
        ps_smoothed = accelerometers.smooth(ps, smooth_window=smooth_when_plot)
        plt.figure()
        plot_util.generic_plot(np.log10(ps_smoothed[accelerometers.POWER_LABEL]), kind='line', xlabel='Hz', ylabel='log10(W/kg/Hz)',
                               title=title, output_directory=outputdir)
        plt.close()

    # Log power spectrum, logged x
    if not pathlib.Path(outputdir / (title + '_logx.png')).exists():
        ps_smoothed = accelerometers.smooth(ps, smooth_window=smooth_when_plot)
        plt.figure()
        plot_util.generic_plot(np.log10(ps_smoothed[accelerometers.POWER_LABEL]).rename(np.log10, axis=0), kind='line', xlabel='log10(Hz)', ylabel='log10(W/kg/Hz)',
                               title=title + '_logx', output_directory=outputdir)
        plt.close()

    total_pow = np.trapezoid(ps[accelerometers.POWER_LABEL], x=ps.index)
    tot_pow_collection[title] = total_pow
    g_collection[title] = df['g-force'].mean()

    print('Total Power: ' + str(int(total_pow)) + ' W/kg')
    print('Mean g-force: ' + str(df['g-force'].mean().round(2)) + " g's")

print(len(ps_collection))

combined = accelerometers.interp_combine(ps_collection)

combined.to_csv(outputdir / 'Combined.csv')

agg_stats_df = pd.DataFrame(index=['Power [W/kg]', 'g-force [-]'], columns=combined.columns)
idx = pd.IndexSlice
for col in combined:
    agg_stats_df.loc[idx['Power [W/kg]'], idx[col[0], col[1]]] = tot_pow_collection[col[0] + accelerometers.DELIMITTER + col[1]]
    agg_stats_df.loc[idx['g-force [-]'], idx[col[0], col[1]]] = g_collection[col[0] + accelerometers.DELIMITTER + col[1]]
print(agg_stats_df.T)

agg_stats_df.to_csv(outputdir / 'Aggregate Stats by Trip.csv')

# Take the log before the average to avoid domination of occasional noise
# Equivalent to geometric rather than arithmetic mean
# Smooth after averaging
combined_bycat_log = accelerometers.smooth(combined.map(np.log10).groupby('Category', axis=1).mean(), smooth_when_plot)
plot_util.generic_plot(combined_bycat_log.rename(np.log10, axis=0), kind='line', xlabel='log10(Hz)', ylabel='log10(W/kg/Hz)',
                       output_directory=outputdir, title='Average Power Spectra by Mode')

grouped_stats = agg_stats_df.T.groupby(level=0).mean()
grouped_stats.to_csv(outputdir / 'Grouped Aggregated Stats by Trip.csv')
print(grouped_stats)

print('Standard Errors')
z_grouped_stats = (agg_stats_df.T.groupby(level=0).std() / agg_stats_df.T.groupby(level=0).mean()).map(lambda x: np.round(x, 2))
z_grouped_stats.to_csv(outputdir / 'Z for Grouped Agg Stats by Trip.csv')
print(z_grouped_stats)
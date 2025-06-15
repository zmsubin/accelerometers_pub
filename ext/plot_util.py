# This has a generic plotting function for line, bar, and stacked area in matplotlib.
# Also a histogram setup for smooth line-based histograms.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
import warnings


TICKWARN = "set_ticklabels"


def generic_plot(data, kind='bar', unstacked=False, color=None, title='', ylabel='', xlabel='',
                 fontsize=12, filename=None, output_directory='', fmt='png', rot=0, ylim=None, style=None, legend=True,
                 long_labels=False, linestyle=None, colormap=None, xlim=None, logx=False, logy=False):
        
    
    if (kind == 'bar' or kind == 'area' or kind == 'barh') and unstacked == False:
        stacked = True
    else:
        stacked = False
    if color is not None:
        if linestyle:
            ax = data.plot(kind=kind, fontsize=fontsize, stacked=stacked, color=color, rot=rot, style=style, legend=legend,
                linestyle=linestyle, cmap=colormap)
        else:
            ax = data.plot(kind=kind, fontsize=fontsize, stacked=stacked, color=color, rot=rot, style=style, legend=legend,
                          cmap=colormap)
    else:
        if linestyle:
            ax = data.plot(kind=kind, fontsize=fontsize, stacked=stacked, rot=rot, style=style, legend=legend,
                linestyle=linestyle, cmap=colormap)
        else:
            ax = data.plot(kind=kind, fontsize=fontsize, stacked=stacked, rot=rot, style=style, legend=legend,
                          cmap=colormap)
    ax.set_title(title, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    ax.set_xlabel(xlabel, fontsize=fontsize)

    if rot == 0 and kind == 'bar' and not long_labels:
        # xtick_labels = ax.get_xticklabels()
        xtick_labels = [re.sub(' ', '\n', str(x)) for x in data.index]
        ax.set_xticklabels(xtick_labels, fontsize=fontsize - 2)

    if logx:
        warnings.filterwarnings("ignore", message=TICKWARN)
        ticks = ax.get_xticks()
        ax.set_xticklabels(['$10^{' + str(x) + '}$' for x in ticks])

    if logy:
        warnings.filterwarnings("ignore", message=TICKWARN)
        ticks = ax.get_yticks()
        ax.set_yticklabels(['$10^{' + str(x) + '}$' for x in ticks])

    if legend:
        handles, labels = ax.get_legend_handles_labels()
        ldg = [ax.legend(handles=handles[::-1], labels=labels[::-1], fontsize=fontsize, bbox_to_anchor=[1, 1])]
    else:
        ldg = []

    if ylim is not None:
        ax.set_ylim(ylim)
    
    if xlim is not None:
        ax.set_xlim(xlim)

    if filename is None:
        if title == '':
            raise RuntimeError('Either title or filename must be specified')
        else:
            filename = title
    
    plt.savefig(os.path.join(output_directory, filename + '.' + fmt),
                format=fmt, bbox_extra_artists=ldg,
                bbox_inches='tight', dpi=600)
    return ax


def shade(ax, group_size, num_bars):
    for i in np.arange(-0.5, -0.5 + num_bars, group_size):
        if (i + 0.5) / group_size % 2 == 0:
            ax.fill_betweenx(np.arange(ax.get_ylim()[0], ax.get_ylim()[1]), i, i + group_size, zorder=0,
                             facecolor='gainsboro', alpha=1)
        else:
            pass
    return ax


def smooth_hist_for_plot(data, label='Data', weights=None, bins=None):
    # Smooth histogram with matched dimensions for plotting
    # Example:
    # indices = np.arange(0, 50, 1)
    # hist_df = plot_util.smooth_hist_for_plot(vmt_cap_pop['residentialVMT_perCapita'], bins=indices)
    # hist_df.plot()
    if bins is None:
        bins = np.arange(data.min(), data.max(), (data.max() - data.min()) / 50)
    hist = np.histogram(data, weights=weights, bins=bins)
    hist_df = pd.DataFrame(index=hist[1][:-1], data=hist[0])
    hist_df = hist_df.rename({0: label}, axis=1)
    return hist_df
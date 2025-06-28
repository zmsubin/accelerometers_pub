# Functions for processing output from Sensor Logger and making power spectrum charts.
# See app info at https://www.tszheichoi.com/sensorlogger.

import pandas as pd
import numpy as np


# Constants and file column conventions for Accelerometer.csv
GRAV = 9.8 # m/s^2
COORDS = ['x', 'y', 'z']
TIME = 'seconds_elapsed'
FREQ_LABEL = 'Frequency'
POWER_LABEL = 'Smoothed Power'
DELIMITTER = '--'
MODE_KEY_PATH = 'ModeKey.csv'
MODE_TYPE = 'Mode Type'


# Clean file
def clean_file(filepath, clip=20):
    # filepath is a pathlib path
    # clip is the number of s to clip at the beginning and end, e.g. to cut motion of manipulating phone and putting into pocket, or getting off train.
    # Returns dataframe with x, y, z, g-force
    # Index is sec since start
    data = pd.read_csv(filepath)
    tmin = data[TIME].min()
    tmax = data[TIME].max()
    data = data[data[TIME] >= tmin + clip]
    data = data[data[TIME] <= tmax - clip]
    data = data.set_index(TIME)[COORDS]
    data['g-force'] = np.sqrt(data.apply(lambda x: x**2).sum(axis=1)) / GRAV
    return data


# Smooth
def smooth(data, smooth_window=10):
    # Smooth is an int for the smoothing window
    if smooth_window <= 1:
        return data
    df = data.copy()
    df['step10'] = np.floor(np.arange(len(data)) / smooth_window)
    df = df.reset_index().groupby('step10').mean().set_index(data.index.name)#.drop('step10', axis=1)
    return df


# Power spectrum
def ps(data, smooth_window=10):
    # data is a clean dataframe output from clean_file
    # returns dataframe with smoothed power spectrum
    # Index is frequency in Hz
    # Vals are in units of W/kg/Hz
    df = data[COORDS].apply(lambda x: np.abs(np.fft.rfft(x))**2)

    # Determine timestep
    steps = data.index[1:] - data.index[:-1]
    dt = np.median(steps)
    T = len(steps) * dt # Total T estimated allowing for cuts in recording
    
    # Normalize for recording length and allow physical power spectrum units
    # See https://en.wikipedia.org/wiki/Spectral_density#Units and https://en.wikipedia.org/wiki/Spectral_density#Power_spectral_density
    df *= dt**2 / T
    
    # Retrieve frequency axis
    df[FREQ_LABEL] = np.fft.rfftfreq(len(data), d=dt)
    df = df.set_index(FREQ_LABEL)
    
    # Smooth
    df = smooth(df, smooth_window=smooth_window)
    
    # Calc sum and drop x,y,z
    df[POWER_LABEL] = df.sum(axis=1)
    return df[[POWER_LABEL]]


def interp_combine(ps_col, freq=np.logspace(-1.5, 1.5, 1000)):
    # Interpolate and combine onto a common axis
    # ps collection has keys with labels concatenated by category and DELIMITTER with individual trip
    # Organize with column multi-index and return.
    
    combined = pd.DataFrame(index=freq)
    for title in ps_col.keys():
        ps = ps_col[title].copy()
        combined[title] = np.interp(x=combined.index, xp=ps.index, fp=ps[POWER_LABEL])
        
    combined.columns.set_names('Trip', inplace=True)
    combined.index.set_names('Freq', inplace=True)
    combined = pd.DataFrame(combined.stack()).rename({0: 'Power'}, axis=1)
    combined = combined.reset_index()
    
    combined['Category'] = combined['Trip'].map(lambda x: str.split(x, DELIMITTER)[0])
    combined['SubTrip'] = combined['Trip'].map(lambda x: str.split(x, DELIMITTER)[1])
    
    combined = combined.pivot(index='Freq', columns=['Category', 'SubTrip'], values='Power')
    
    return combined


def mode_map(key):
    # Dictionary of modes read in from file
    df = pd.read_csv(MODE_KEY_PATH, header=0, index_col=0)
    try:
        return df.loc[key][MODE_TYPE]
    except KeyError:
        return key


def mode_match(keys, val):
    # Return list of keys that match val using mode_map
    # keys is iterable
    subset = []
    for key in keys:
        if mode_map(key) == val:
            subset.append(key)
    return subset


def pow_range(df, bounds=[10**(-0.5), 10**(0.75)], unlogged=False,
              range_names=['Bulk Acceleration', 'Oscillation', 'Vibration']):
    # Integrated power over a frequency range
    # df is an already logged (by default) power spectrum
    # bounds must have length 1 less than range_names
    
    if len(bounds) != len(range_names) - 1:
        raise ValueError

    if unlogged:
        df = df.map(np.log10)
    
    pow_seg = pd.DataFrame(index=np.arange(len(bounds)+1), columns=df.columns)
    for i in pow_seg.index:
        if i == 0:
            islice = df.index <= bounds[i]
        elif i < len(bounds):
            islice = (df.index > bounds[i-1]) & (df.index <= bounds[i])
        else:
            islice = df.index > bounds[i-1]
        segment = df.loc[islice]
        for col in pow_seg.columns:
            pow_seg.loc[i, col] = np.trapezoid(10**segment[col], x=segment.index)

    pow_seg = pow_seg.rename({i: range_names[i] for i in range(len(range_names))})
    return pow_seg
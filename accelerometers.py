# Functions for processing output from Sensor Logger and making power spectrum charts.
# See app info at https://www.tszheichoi.com/sensorlogger.

import pandas as pd
import numpy as np
import pathlib


# Constants and file column conventions for Accelerometer.csv
GRAV = 9.8 # m/s^2
COORDS = ['x', 'y', 'z']
TIME = 'seconds_elapsed'
FREQ_LABEL = 'Frequency'
POWER_LABEL = 'Smoothed Power'


# Clean file
def clean_file(filepath):
    # filepath is a pathlib path
    # Returns dataframe with x, y, z, g-force
    # Index is sec since start
    data = pd.read_csv(filepath)
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
    
    # Normalize for physical power spectrum units
    # See https://en.wikipedia.org/wiki/Spectral_density#Units and https://en.wikipedia.org/wiki/Spectral_density#Power_spectral_density
    df *= dt**2
    
    # Retrieve frequency axis
    df[FREQ_LABEL] = np.fft.rfftfreq(len(data), d=dt)
    df = df.set_index(FREQ_LABEL)
    
    # Smooth
    df = smooth(df, smooth_window=smooth_window)
    
    # Calc sum and drop x,y,z
    df[POWER_LABEL] = df.sum(axis=1)
    return df[[POWER_LABEL]]
# accelerometers
Functions for processing output from Sensor Logger and making power spectrum charts.
The goal of this project is to measure acceleration and vibration (i.e., higher frequency acceleration)
on various transportation modes to understand and document motion sickness triggers.

See app info at https://www.tszheichoi.com/sensorlogger.
And https://github.com/tszheichoi/awesome-sensor-logger/.

Workflow: Save trips with "Accelerometer" toggled as the included sensor. (You'll need to enable location tracking in the background for the app
on iOS, and it's useful to save location too for trip naming and reconstruction if needed.) Save the files in subfolders with the mode or other category desired. Move output zips to ignored input directory; run unzip.sh, adjusting paths if needed; use analyze_functionalized as a script make plots for new files and print stats and summary plot. explore_analyzed allows for custom plots in a notebook.

IF YOU ARE CHECKING IN CODE and using notebooks make sure to restart kernel and clear outputs, or otherwise mask your location, to avoid checking in personal
location info. The code is written to not reference any filenames or trip titles directly as variable names or literal strings.

Currently analyze_functionalized is not optimized for large numbers of trips, as it loads each file into memory and stores in a large dictionary. For future
development files could be first merged onto the (much sparser) interpolated output dataframe and then cleared from memory; or the output could be designed
to be built up incrementally over time in timestamped files and merged in another plotting script.

## ext
Zack's handy plotting functions.

## inputdata
Put gitignored input files here.

## outputdata
Output figs will appear here.

## scratch
Testing

## accelerometers.py
Module for cleaning and calculating Power Spectrum

## analyze_functionalized.py
Driver script

## explore_analyzed.ipynb
Additional user-customized plots

## unzip.sh
Adapted a bash script from Stack Overflow -- use at your own risk.
# accelerometers
Functions for processing output from Sensor Logger and making power spectrum charts.
The goal of this project is to measure acceleration and vibration (i.e., higher frequency acceleration)
on various transportation modes to understand and document motion sickness triggers.

See app info at https://www.tszheichoi.com/sensorlogger.
And https://github.com/tszheichoi/awesome-sensor-logger/.

Workflow: Move output zips to ignored input directory; run unzip.sh, adjusting paths if needed; use analyze_functionalized to make plots for
one trip (file) at a time and print stats.

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

## analyze_functionalized.ipynb
Driver notebook

## unzip.sh
Adapted a bash script from Stack Overflow -- use at your own risk.
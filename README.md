# accelerometers
Functions for processing output from Sensor Logger and making power spectrum charts.
The goal of this project is to measure acceleration across frequency ranges
on various transportation modes to understand and document motion sickness triggers.

See app info at https://www.tszheichoi.com/sensorlogger.
And https://github.com/tszheichoi/awesome-sensor-logger/.
Technical note in "writeup/", viewable on the [online repo](https://github.com/zmsubin/accelerometers_pub/blob/main/writeup/TechNote.md).

Workflow:
1. Export recordings with "Accelerometer" toggled as an included sensor at 100 Hz or as high as allowed.
    * You'll need to enable location tracking in the background for the app
on iOS, and it's useful to save location too for trip naming and reconstruction if needed. Try to keep each recording to ~>5-10 min and as much as possible limited to a single activity with a constant phone position.
2. Save the files in subfolders with the mode or other category desired. Move output zips to ignored input directory defaulting to "inputdata/".
3. Run unzip.sh from the inputdata directory, adjusting paths if needed.
4. Adjust ModeKey.csv to customize the meta-categories of trip modes or activities.
5. Run analyze_functionalized as a command-line python script ("python analyze_functionalized.py") to make plots for new files and print stats and summary plot.
6. (Optional) Make additional custom plots using explore_analyzed in a notebook.

**If you are checking in code** and using notebooks, make sure to restart kernel and clear outputs, or otherwise mask your location, to avoid checking in personal
location info. The code is written to not reference any filenames or trip titles directly as variable names or literal strings.

Currently analyze_functionalized is not optimized for large numbers of trips, as it loads each file into memory and stores in a large dictionary. It's currently working fine for several dozen trips on a 16 GB RAM Mac mini. For future
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

## example_outputs
Sample figures

## writeup
Technical note

## accelerometers.py
Module for cleaning and calculating Power Spectrum

## analyze_functionalized.py
Driver script

## explore_analyzed.ipynb
Additional user-customized plots

## unzip.sh
Adapted a bash script from Stack Overflow -- use at your own risk.

## ModeKey.csv
Dictionary of mode types to analyze (major categories above the minor mode categories implemented in subfolders).
# Technical Note: Analysis of Acceleration during Trips and Activities

This code analzyes output from the [Sensor Logger app](https://www.tszheichoi.com/sensorlogger) 
"Accelerometer" sensor for many recordings at once. This sensor reports calibrated linear acceleration after subtracting the gravity vector (so it is zero when stationary on the earth's surface).

Each recording should represent a single trip or activity, at least ~5 minutes in duration, organized by travel mode or activity category. The phone should be kept in pocket or a constant bodily position as much as possible for the duration of the trip. Because power spectra and vector-norm acceleration are reported, the results should be insensitive to the phone orientation except for very rapid rotation. (The total power spectrum is a linear combination of spatial-component power spectra.) The analysis reports individual and averaged trip acceleration and power spectra, to compare characteristic movement for modes.

## Normalized acceleration ([g-force](https://en.wikipedia.org/wiki/G-force))

The normalized acceleration $A_\tau(t)$ at time $t$ for trip $\tau$ is:

```math
A_\tau(t) = \frac{1}{g}{\sqrt{a_x^2(t) + a^2_y(t) + a^2_z(t)}}_\tau = \frac{1}{g}\|\vec{a}(t)\|_\tau
```

where $\vec{a}$ [m s $^{-2}$] is the vector linear acceleration  (over each spatial component $x, y, z$) and $g = 9.8$ m s $^{-2}$.

## Power spectrum

The [power spectrum](https://en.wikipedia.org/wiki/Spectral_density) $S_\tau(f)$ [W kg $^{-1}$ s] at frequency $f$ for trip $\tau$ is:

```math
S_\tau(f) = \Delta t^2 \left(|\hat{a}_x|^2 + |\hat{a}_y|^2 + |\hat{a}_z|^2\right) _\tau
```

where $\hat{a}_{x,y,z}$ is the Real [Discrete Fourier Transform](https://en.wikipedia.org/wiki/Discrete_Fourier_transform) of the acceleration for each spatial component and $\Delta t$ [s] is the timestep. The Real Discrete Fourier Transform is evaluated using the _numpy_ functions "rfft" and "rfftfreq."

## Log-mean power spectrum

The log-mean (i.e., geometric mean) power spectrum $\bar{S}_m(f)$ for each mode $m$ is:

```math
\log_{10}{\bar{S}_m(f)} = \frac{\sum_{\tau \in m}{\log_{10}S_\tau(f)}}{N_m}
```

where $N_m$ is the number of trips $\tau$ on the mode $m$.

## Integrated power

The integrated power $P$ [W kg $^{-1}$] from frequency $f_1$ to $f_2$ is:

```math
P = \int_{f_1}^{f_2}S(f)df
```

where $S(f)$ is a power spectrum or mean power spectrum. The integral should be performed over the unlogged power; when integrating the log-mean power spectrum defined above it is first exponentiated:

```math
P = \int_{f_1}^{f_2}10^{\log_{10}\bar{S}_m(f)}df .
```



## Cleaning, smoothing, and interpolation

Each trip is clipped at the beginning and end, by a default of 20 s. Normalized acceleration and power spectrum plots are smoothed by averaging over a default of 100 timesteps or frequency increments, respectively.

To limit file size and facilitate averaging and comparison across trips, power spectra are interpolated, after smoothing, onto a common frequency range, default log-spaced from 0.1 to 32 $(10^{1.5})$ Hz with 1000 increments.

The log-mean averaging of power spectra suppresses noise and outlier trips; however, outlier trips may be removed manually after many trips are compared for a mode or category.


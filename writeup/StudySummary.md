# A Personal Study of Oscillation on Transportation and Daily Activities

[Zack Subin](https://github.com/zmsubin)

**DRAFT**: _Last Updated Jan 3, 2026_

## Background and Findings

I am an urbanist living in San Francisco. My husband and I share one car, and I use active and public transportation for nearly all my daily activities. Since 2012, I've had chronic migraine, which makes me especially susceptible to motion sickness (a consequence of a crash at a poorly designed Berkeley intersection\- but that's a subject for another article!).

I have experienced consistent discomfort while riding BART since the pandemic, during which BART completed its train fleet replacement. Since 2023, I have been commuting to downtown Oakland from Balboa Park Station. I perceive the new train cars have a rougher ride, characterized by sideways oscillation (perpendicular to the direction of travel) which is especially bad on higher-speed segments such as the Transbay Tube. Some rides are definitely worse than others, but it is a widespread problem I notice on most. I do not remember this level of discomfort in prior BART rides during my 20 years living in the Bay Area, including daily commutes from Balboa Park to Montgomery Stations from 2018 through spring 2020. I have reported my experience to BART via multiple contact methods but no confirmation was provided nor action taken.

In May 2025, I became curious to see if I could measure the bothersome behavior myself using [Sensor Logger](https://www.tszheichoi.com/sensorlogger), a freemium app developed by physicist and transportation engineer Kelvin Choi. Since May I have recorded and analyzed over 250 activity segments, including over 160 BART rides.

While continuing to collect data, **I preliminarily conclude that BART has a ubiquitous oscillation with a peak near 1.8 Hz, which I do not observe on other modes of transit. I hypothesize this is due to [Hunting Oscillation](https://en.wikipedia.org/wiki/Hunting_oscillation) in the new train cars**, perhaps because these reverted to conventional conical wheels unlike BART's [original cylindrical wheels](https://www.bart.gov/news/articles/2018/news20180606), unmasking other  Hunting contributors.

![Line chart showing mid-range peak for BART relative to other trains](Figure1.png)

I expand below. Readers may also refer to the accompanying Technical Note briefly documenting the analysis code.

## Introduction: why analyze acceleration power spectra?

## Analysis

### Acceleration Power Spectra

### Comparing BART with other Trains

### Other Travel Modes; Positive and Negative Controls

## A Disclaimer

My motivation for this exercise is mostly the fun of a little citizen science and coding project, with modest hope my methods may be applicable to health and transportation researchers, or to other citizen scientists and advocates susceptible to motion sickness. It _would_ be nice if BART validated my experience by admitting a specific engineering problem - especially if this exercise leads other riders to note similar experiences. However, I am under no illusions that BART can feasibly fix any noncritical problems, even if widespread, in the near future. The most important priority for Bay Area transit advocates in 2026 is securing long-term financing for BART and other transit systems.

Finally, while I have physical science training, I am not qualified as a transportation engineer nor health scientist, so I invite others to replicate my findings.

## Appendix

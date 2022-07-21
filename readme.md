# IMUK synoptic weather wall

Using opendata from the dwd to visualize and display synoptic Data

## Parameters for Groundlevel
Here are different parameters used to display the groundlevel documented.

### Recommended 
#### Past
- CLCT_MOD:  cloud coverage
- PMSL: reduced surface pressure
- WW:  significant weather

#### Future
- PWSL: reduces surface pressure
- CLCT_MOD: cloud coverage
- TOT_PREC: total Precipitation

### En detail
#### Clouds
Different Methods available:

- CLC: Cloud Cover in a single level. Multi Level
- CLCT: Total cloud cover with cirrus. Single Level
- CLCT_MOD: Modified total cloud cover, effective CLC without Cirrus. Greyscale. Single Level. Often Used in media

-Meteosat HRV/IR 10.8 Original used Satellite Data

#### Pressure
- PS: Surface pressure (not reduced). Single Level
- PMSL: Surface pressure reduced to MSL. Single Level

#### Significant weather

WW: Significant weather of the last hour. Single Level

#### Precipitation

- TOT_PREC: Total precipitation accumulated since model start

- 3h Total precipitation accumulated original used 
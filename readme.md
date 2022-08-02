# IMUK synoptic weather wall

Using opendata from the dwd to visualize and display synoptic Data


## Colorscale for 700 hPa
- 1-7: rgba(254, 255, 69, 1): (0.99,1,0.27,1 )
- -7.5-15 rgba(254, 253, 134, 1)(0.99,0.99,0.52,1)
- 15-22,5 rgba(254, 255, 221, 1) (0.99,0.99,0.87,1)
- 22.5 -30 rgba(253, 255, 242, 1) (0.99,0.99,0.95,1)
- 30-60 (1,1,1,0)
- 60-67.5 rgba(55, 217, 56, 1) (0.22,0.85,0.22)
- 67.5-75
- 75-82,5 
- 82,5-90
- 90-95
- 95-100 rgba(0, 119, 159, 1)(0,0.47,0.62)
## Colorscale for 300 hPa

- 1-30:Transparent 
- 31-40 : Green #33ff00
- 41-50:  Cyan #21e8ff
- >50 : Magenta #fe00fe

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
- Meteosat HRV/IR 10.8 Original used Satellite Data

#### Pressure
- PS: Surface pressure (not reduced). Single Level
- PMSL: Surface pressure reduced to MSL. Single Level

#### Significant weather

- WW: Significant weather of the last hour. Single Level

#### Precipitation

- TOT_PREC: Total precipitation accumulated since model start

- 3h Total precipitation accumulated original used 

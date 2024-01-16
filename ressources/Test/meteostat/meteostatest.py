# Import Meteostat library and dependencies
from datetime import datetime
from meteostat import Hourly
import pandas as pd
from meteostat import Stations
import warnings
warnings.filterwarnings("ignore")
from ressources.tools.imuktools import nclwwstring

# Set time period
start = datetime(2023, 3, 22,0,0)
end = datetime(2023, 3, 22, 0, 0)
stations = Stations()
#stations = stations.region('DE')
stations = stations.bounds((62, -45), (35, 45)) # Stations in Europe
#stations = stations.inventory('hourly', [start,end])
stations = stations.fetch()#(2, sample=True)#stations.fetch()#
datawwfont = pd.read_csv('../../Data/wwfont.csv')  # Fontframe

#print(stations.index)


# Get hourly data
data = Hourly(stations, start, end)
data = data.fetch()
list_of_stations = []
lon = []
lat = []
weatherfont=[]
weathersymbol=[]
weathercolour=[]
nclstring=[]

for x in data.index:
    print(x)
    list_of_stations.append(x[0])
    lat.append(stations["latitude"].loc[x[0]])
    lon.append(stations["longitude"].loc[x[0]])
    try :
        wwcode = datawwfont.index[datawwfont["Meteostat Code"] == int(data["coco"].loc[x[0]])][0]

    except ValueError :
        wwcode=0

    #print(wwcode)
    try :
        weatherfont.append(datawwfont.iloc[wwcode]["font"])#int(data["coco"].loc[x[0]])]["font"]

    except ValueError :
        weatherfont.append(None)

    try :
        weathersymbol.append(datawwfont.iloc[wwcode]["letter"])

    except ValueError :
        weathersymbol.append(None)

    try :
        weathercolour.append(datawwfont.iloc[wwcode]["colour"])

    except ValueError :
        weathercolour.append(None)


# Transformations for  NCL
data=data.assign(lat=lat,lon=lon,weatherfont=weatherfont,weathersymbol=weathersymbol,weathercolour=weathercolour)
nclstring= nclwwstring(data)
#data=data.dropna()
## Lat/long:
#print(list_of_stations)
print(data)
data=data.to_csv('meteostatdata.csv', index=True)
#print(stations[stations.index == data["station"==10400]])

# Print DataFrame

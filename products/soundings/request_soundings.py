import requests
import zipfile
import os 
from glob import glob

oldcwd=os.getcwd()

newcwd = oldcwd +"/products" +"/soundings"
os.chdir(newcwd)

def request(stationid="00368"):
    r = requests.get('https://opendata.dwd.de/climate_environment/CDC/observations_germany/radiosondes/high_resolution/recent/sekundenwerte_aero_'+stationid+'_akt.zip')
    if r.status_code != 200:
        raise Exception("Data can't be requested: ",r.status_code)
    else:
        with open("temp.zip", "wb") as file:
            file.write(r.content)

        with zipfile.ZipFile("temp.zip", "r") as zip_ref:
            zip_ref.extractall("sounding_data")

        files= glob("sounding_data/*"+stationid+"*")
        os.rename(files[0], 'sounding_data/sounding_'+stationid+'.txt')
    return

request()
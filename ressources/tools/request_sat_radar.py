import os, sys
import warnings
from IPython.core.display import HTML
from IPython.display import Image
from owslib.wms import WebMapService
from owslib.util import Authentication
from skimage import io
import requests
import authorisation_functions as auth
from datetime import datetime, timedelta
import pyproj
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import rasterio
from rasterio.plot import show
import numpy as np
import cartopy.feature as cfeature
import os
import wradlib as wrl
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
import xarray as xr
from matplotlib.colors import LinearSegmentedColormap
from scipy import ndimage
import os
import wradlib as wrl
import matplotlib.pyplot as plt
import warnings
import time


import numpy as np
import xarray as xr
warnings.simplefilter("ignore")

oldcwd=os.getcwd()
#PYPROJ_GLOBAL_CONTEXT=ON
newcwd = oldcwd +"/products" +"/satelite"
os.chdir(newcwd)

print(oldcwd)
print(newcwd)

def reqeuest_satelite(timestart,timeend,time_file,visible=False, bbox=(-70, 24, 70, 72),sizemulti=1, filename="hans"):
    credentials = auth.import_credentials('credentials.json')
    access_token = auth.generate_token(consumer_key=credentials['consumer_key'],
                                       consumer_secret=credentials['consumer_secret'])
    print('Access token retrieved: ' + access_token)

    service_url = 'https://view.eumetsat.int/geoserver/ows?'
    wms = WebMapService(service_url, auth=Authentication(verify=False))
    if visible:
        target_layer = 'msg_fes:vis006'
        file_loc="vis"
    else:
        target_layer = 'msg_fes:ir108'  # 'msg_fes:rgb_natural'
        file_loc="ir"


    format_option = 'image/geotiff'

    payload = {
        'layers': [target_layer],
        'styles': '',
        'format': format_option,
        'crs': 'EPSG:4326',
        'bbox': bbox,#(-70, 24, 70, 72),
        'size': (sizemulti*945, sizemulti*945),
        'time': timestart+"/"+timeend
    }

    wms = WebMapService(service_url, auth=Authentication(verify=False))
    #img = wms.getmap(**payload)

    max_attempts = 5

    # Starte einen Versuchscounter
    attempt = 0

    # Schleife zum Wiederholen der Anfrage
    while attempt < max_attempts:
        try:
            # Führe die Datenanfrage aus
            img = wms.getmap(**payload)
            
            # Überprüfe, ob die Anfrage erfolgreich war (Statuscode 200)
            attempt = max_attempts
        
        except Exception as e:
            # Fangen andere mögliche Fehler ab, z.B. Verbindungsfehler
            print(f"Fehler beim Abrufen der Daten: {e}")
            attempt += 1
            print(f"Warte 5 Sekunden vor dem nächsten Versuch...")
            time.sleep(5)  # Warte 5 Sekunden, bevor der nächste Versuch gestartet wird










    Image(img.read())
    with open(oldcwd+"/database/input/satelite/"+file_loc+"/"+filename+'.tiff', 'wb') as f:
        f.write(img.read())

    return



def reqeuest_radar(timer,filename="latest"):
    #url_base = "https://opendata.dwd.de/weather/radar/radolan/yw/"
    #url_data = url_base +'raa01-yw_10000-{}-dwd---bin.bz2'.format(timer)
    url_base = "https://opendata.dwd.de/weather/radar/radolan/ry/"
    url_data = url_base +'raa01-ry_10000-{}-dwd---bin.bz2'.format(timer)
    print(url_data)
    #url_data = "https://opendata.dwd.de/weather/radar/radolan/yw/raa01-yw_10000-latest-dwd---bin.bz2"
    #print(url_data)
    
    data_request = requests.get(url_data, stream=True)
    #p#rint(data_request.content)
   # if data_request.status_code == 200:
     #   print(url_data)


    with open(oldcwd+'/database/input/radar/radar_'+filename+".bz2", 'wb') as f:
        f.write(data_request.content)

    try:
        os.remove(oldcwd+'/database/input/radar/radar_'+filename)
    except FileNotFoundError:
        pass
    zip_command = 'bzip2 -d '+ oldcwd+'/database/input/radar/radar_'+filename+'.bz2'
    os.system(zip_command)
    #os.remove(oldcwd+'/database/input/radar/radar_'+filename+'.bz2')

    return


def multi_request_all(latest_datetime):

    print(latest_datetime)
    datetimes_list = [latest_datetime - timedelta(minutes=15 * i) for i in range(0, 96)] # Last 24 hours in 15 min increments 

    # Ausgabe der Liste
    print(datetimes_list)

    for number  in range(len(datetimes_list)):
        date = datetimes_list[number]
        filename = "latest_T-"+str(number)
        radar_date = date.strftime('%y%m%d%H%M')
        print(date)
        times = date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        time  = date.strftime('%Y-%m-%d %H:%M:%S')
        reqeuest_satelite(times,times,time,visible=True,sizemulti=2, filename=filename)
        reqeuest_satelite(times, times, time, visible=False,sizemulti=2,filename=filename)
        reqeuest_radar(radar_date, filename=filename)


    return


def multi_request_one(latest_datetime):
    print(latest_datetime)
    folders = [oldcwd+"/database/input/satelite/ir", oldcwd+"/database/input/satelite/vis",oldcwd+"/database/input/radar/"]
    adds = [".tiff",".tiff",""]
    for folder, add in zip( folders,adds):
        folder_path = os.path.join(os.getcwd(), folder)
        for i in range(11, -1, -1):
            old_filename = os.path.join(folder_path, f"latest_T-{i}"+add)
            new_filename = os.path.join(folder_path, f"latest_T-{i+1}"+add)
            
            if os.path.exists(old_filename):
                os.rename(old_filename, new_filename)
            

                # Löschen der Datei latest_T-12, falls vorhanden
        latest_T_12_path = os.path.join(folder_path, "latest_T-12"+add)
        if os.path.exists(latest_T_12_path):
            os.remove(latest_T_12_path)
   

    filename = "latest_T-"+str(0)
    radar_date = latest_datetime.strftime('%y%m%d%H%M"')

    times = latest_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    time  = latest_datetime.strftime('%Y-%m-%d %H:%M:%S')
    reqeuest_satelite(times,times,time,visible=True,sizemulti=2, filename=filename)
    reqeuest_satelite(times, times, time, visible=False,sizemulti=2,filename=filename)
    reqeuest_radar(radar_date, filename=filename)

if __name__ == "__main__":
    datetime_obj = datetime(2024, 4, 22, 12, 0, 0)
    #times = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    #time  = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    #reqeuest_satelite(times,times,time,visible=True,sizemulti=2)
    #reqeuest_satelite(times, times, time, visible=False,sizemulti=2)
    #reqeuest_radar("latest")
    multi_request_all(datetime_obj)
    #multi_request_one(datetime_obj)
    #reqeuest_radar("latest", "latest_T-0")
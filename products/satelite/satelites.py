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

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import rasterio
from rasterio.plot import show
import numpy as np
import cartopy.feature as cfeature


# turn off warnings (suppresses output from certification verification when verify=false)
warnings.simplefilter("ignore")
class satelite_image:
    def __init__(self, target_lat_start,target_lat_end, target_lon_start, target_lon_end,time,name):
        self.lat_start = target_lat_start
        self.lat_end = target_lat_end
        self.lon_start = target_lon_start
        self.lon_end = target_lon_end
        self.time = time
        self.name = name

    def remap(self):
        fig = plt.figure(figsize=(12.8,7.2))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal(
            central_longitude=10))  # ,central_latitude=52) ) #ccrs.Miller())#
        ax.coastlines()
        ax.add_feature(cfeature.LAND, facecolor='darkgreen')
        ax.add_feature(cfeature.OCEAN, facecolor='navy')
        if self.name !="europe":
            ax.add_feature(cfeature.LAKES)
            ax.add_feature(cfeature.COASTLINE)
            ax.add_feature(cfeature.STATES)
            ax.add_feature(cfeature.BORDERS)
        ax.set_extent([self.lon_start, self.lon_end, self.lat_start, self.lat_end], crs=ccrs.PlateCarree())  # Begrenzung auf Europa
        # Kasten am unteren Rand einfügen
        ax.annotate(f'{self.time}', xy=(0.02, 0.04), xycoords='axes fraction',
                    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round',edgecolor="black"),fontsize=14)

        # Weitere Informationen im Kasten hinzufügen (anpassen, wie benötigt)
        additional_info = "EUMETSAT SEVIRI IR10.8μm"
        ax.annotate(additional_info, xy=(0.98, 0.04), xycoords='axes fraction', ha='right',
                    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round',edgecolor="black"),fontsize=14)

        # Lokales GeoTIFF-Bild laden (ersetzen Sie 'lokales_bild.tif' durch den Pfad zu Ihrem GeoTIFF-Bild)
        local_image_path = 'cut.tiff'

        # GeoTIFF-Bild mit Rasterio öffnen
        with rasterio.open(local_image_path) as src:
            local_image = src.read(1)  # Annahme: Das Bild hat eine einzige Bande

            # Helligkeitsschwelle festlegen

        print('Projecting and plotting image...')
        #extent = (self.lon_start,self.lon_end,self.lat_start,self.lat_end)
        extent = (-70, 70, 24, 72)

        cloud_brightness_threshold = 65

        cloud_mask = np.where(local_image > cloud_brightness_threshold, 1, 0)

        # Erstelle das Ausgabebild, in dem nur die Wolken weiß sind (0 bleiben schwarz)
        output_image = np.where(cloud_mask == 1, local_image + 10, np.nan)

        ax.imshow(output_image, origin='upper', transform=ccrs.PlateCarree(), extent=extent, cmap='gray', vmin=0,
                  vmax=255)

        # Berechne den dpi-Wert für die gewünschte Auflösung
        auflösung_breite = 1920
        auflösung_höhe = 1080
        zoll_pro_dpi = 1 / 600  # Standardmäßig etwa 80 dpi pro Zoll
        dpi = max(auflösung_breite / (zoll_pro_dpi * plt.rcParams['figure.figsize'][0]),
                  auflösung_höhe / (zoll_pro_dpi * plt.rcParams['figure.figsize'][1]))
        ax.set_frame_on(False)
        plt.tight_layout()
        plt.savefig(self.name+'/'+self.name+'_'+self.time+'.png', dpi=300)
        return

def request_sats(timestart,timeend):
    credentials = auth.import_credentials('credentials.json')
    access_token = auth.generate_token(consumer_key=credentials['consumer_key'],
                                       consumer_secret=credentials['consumer_secret'])
    print('Access token retrieved: ' + access_token)

    service_url = 'https://view.eumetsat.int/geoserver/ows?'
    wms = WebMapService(service_url, auth=Authentication(verify=False))
    target_layer = 'msg_fes:ir108'  # 'msg_fes:rgb_natural'

    format_option = 'image/geotiff'

    payload = {
        'layers': [target_layer],
        'styles': '',
        'format': format_option,
        'crs': 'EPSG:4326',
        # 'bbox'   : (-77.7699966430664, -77.7699966430664, 77.7699966430664, 77.7699966430664),
        # 'bbox'   : (-45,35,45,62),
        'bbox': (-70, 24, 70, 72),
        'size': (5*945, 5*945),
        #'time': '2023-08-16T22:00:00.000Z/2023-08-16T22:00:00.000Z'
        'time': timestart+"/"+timeend
    }

    wms = WebMapService(service_url, auth=Authentication(verify=False))
    img = wms.getmap(**payload)
    Image(img.read())
    with open('cut.tiff', 'wb') as f:
        f.write(img.read())
    return
def singlemaps():
    datetime_obj = datetime(2023, 9, 1, 12, 0, 0)  # Hier setzen Sie Ihr eigenes datetime-Objekt ein

    times = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    time  = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    request_sats(times,times)

    #print("starting europe")
    #europe = satelite_image( 35, 65,-45, 45,time,"europe")

    #europe.remap()

    #print("starting lower_saxony")
    #lower_saxony = satelite_image( 51.2, 53.9,5.2, 13.,time,"lower_saxony")

    #lower_saxony.remap()


    print("starting hannover")
    hannover = satelite_image(52.117469,52.604716,9,10.5,time,"hannover")

    hannover.remap()
    return
def multimap():
    for quart in range(0,10,1):
        datetime_obj = datetime(2023, 9, 1, 12, 0, 0) - timedelta(minutes=15*quart) # Hier setzen Sie Ihr eigenes datetime-Objekt ein

        times = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
        request_sats(times, times)

        print("starting europe")
        europe = satelite_image( 35, 65,-45, 45,time,"europe")

        europe.remap()

        # print("starting lower_saxony")
        # lower_saxony = satelite_image( 51.2, 53.9,5.2, 13.,time,"lower_saxony")

        # lower_saxony.remap()

        #print("starting hannover")
        #hannover = satelite_image(52.117469, 52.604716, 9, 10.5, time, "hannover")

        #hannover.remap()
    return

multimap()

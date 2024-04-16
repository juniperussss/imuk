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
#from PIL import Image
import warnings
import seaborn as sns
import xarray as xr
#import gdal
from matplotlib.colors import LinearSegmentedColormap
from scipy import ndimage
import os
import wradlib as wrl
import matplotlib.pyplot as plt
import warnings
import time

import numpy as np
import xarray as xr


# turn off warnings (suppresses output from certification verification when verify=false)
warnings.simplefilter("ignore")

oldcwd=os.getcwd()
#PYPROJ_GLOBAL_CONTEXT=ON
newcwd = oldcwd +"/products" +"/satelite"
os.chdir(newcwd)
def image_brigtness(cloud_brightness_threshold,time,visible=False,radar=False): #,region

    if visible:
        local_image_path = 'baseimages/vis/'  +time + '.tiff' #+ region +'/'+ 
    elif radar:
        local_image_path = 'baseimages/radar/geotiff_n.tiff'
    else:
        local_image_path = 'baseimages/ir/'+ time + '.tiff'

    # GeoTIFF-Bild mit Rasterio öffnen
    with rasterio.open(local_image_path) as src:
        local_image = src.read(1)  # Annahme: Das Bild hat eine einzige Bande

    #cloud_brightness_threshold = 65

    cloud_mask = np.where(local_image > cloud_brightness_threshold, 1, 0)
    output=np.where(cloud_mask == 1, local_image + 10, np.nan)
    return output

def radarrconvertrio():
    import matplotlib.pyplot as plt
    import os
    import wradlib as wrl
    import xarray as xr
    import numpy as np
    import warnings
    from pyproj.crs import CRS

    warnings.filterwarnings("ignore")

    #filename ="DE1200_RV2309181430_000"
    filename = "radar/DE1200_RV2310111815_000"
    #filename = wrl.util.get_wradlib_data_file(filename)
    ds = xr.open_dataset(filename, engine="radolan")
    #print(ds)
    # This is the RADOLAN projection
    proj_osr = wrl.georef.create_osr("dwd-radolan")
    crs = CRS.from_wkt(proj_osr.ExportToWkt(["FORMAT=WKT2_2018"]))
    #print(proj_osr)
    #ds.RV.encoding = {}
    #ds = ds.rio.write_crs(crs)
    #ds.RV.rio.to_raster(wdir + "geotiff_rio.tif", driver="GTiff")


    # Get projected RADOLAN coordinates for corner definition
    xy_raw = wrl.georef.get_radolan_grid(1200, 1100)
    xy_raw.shape
    data, xy = wrl.georef.set_raster_origin(ds.RV.values, xy_raw, "upper")
    print(data.shape)
    # create 3 bands
    data = np.stack((data, data + 100, data + 1000), axis=0)
    print(data.shape)
    gds = wrl.georef.create_raster_dataset(data, xy, crs=proj_osr)
    wrl.io.write_raster_dataset("baseimages/radar/geotiff_n.tiff", gds, driver="GTiff")
    return



def radarrconvert():
    import wradlib as wrl
    import numpy as np
    import warnings
    warnings.filterwarnings('ignore')
    print( wrl.__version__ )

    # We will export this RADOLAN dataset to a GIS compatible format
    #wdir = wrl.util.get_wradlib_data_path() #+ '/radolan/grid/'
    #filename = 'radolan/misc/raa01-sf_10000-1408102050-dwd---bin.gz'

    filename ="DE1200_RV2309181430_000"
    #filename = "raa01-rw_10000-latest-dwd---bin"
    #filename = wrl.util.get_wradlib_data_file(filename)
    #data_raw, meta = wrl.io.read_radolan_composite(filename)

    data_raw = wrl.io.open_radolan_dataset(filename).RV
    # This is the RADOLAN projection
    proj_osr = wrl.georef.create_osr("dwd-radolan")

    # Get projected RADOLAN coordinates for corner definition
    #xy_raw = wrl.georef.get_radolan_grid(900, 900)
    xy_raw = wrl.georef.get_radolan_grid(1200, 1100)

    data, xy = wrl.georef.set_raster_origin(data_raw, xy_raw, 'upper')


    # create 3 bands
    data = np.stack((data, data + 100, data + 1000), axis=0)
    ds = wrl.georef.create_raster_dataset(data, xy, crs=proj_osr)
    wrl.io.write_raster_dataset("baseimages/radar/geotiff_n.tiff", ds, driver='GTiff')
    return 

class satelite_image:
    def __init__(self, target_lat_start,target_lat_end, target_lon_start, target_lon_end,time,name,export_path,radar=False): #region,bbox,
        self.lat_start = target_lat_start
        self.lat_end = target_lat_end
        self.lon_start = target_lon_start
        self.lon_end = target_lon_end
        self.time = time
        self.name = name
        self.radar=radar
        self.export_path = export_path
        #self.bbox =bbox
        #self.region = region
    def remap(self):
        fig = plt.figure(figsize=(12.8,7.2))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal(
            central_longitude=10))  # ,central_latitude=52) ) #ccrs.Miller())#
        pyproj.set_use_global_context()
        #ax.coastlines()
        #ax.LAKES()
        ax.add_feature(cfeature.COASTLINE)
        #ax.add_feature(cfeature.LAND)#, facecolor='darkgreen')
        land_110m = cfeature.NaturalEarthFeature('physical', 'land', '10m',
                                        edgecolor='face',
                                        facecolor="darkgreen",#cfeature.COLORS['land'],
                                        zorder=0)
        ax.add_feature(land_110m)


        ocean_110m = cfeature.NaturalEarthFeature('physical', 'ocean', '110m',   edgecolor='face',  facecolor="navy",               zorder=0)
        ax.add_feature(ocean_110m)
        #ax.add_feature(cfeature.OCEAN)#, facecolor='navy')
        if self.name =="lower_saxony":
            ax.add_feature(cfeature.STATES)
        elif self.name == "hannover":
            ax.add_feature(cfeature.STATES)
            rivers_10m = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m',
                                edgecolor='face',
                                facecolor="blue",#cfeature.COLORS['water'],
                                zorder=0)
            lake_10m = cfeature.NaturalEarthFeature('physical', 'lakes', '10m',
                                edgecolor='face',
                                facecolor="blue",#cfeature.COLORS['water'],
                                zorder=0)
            urban_10m = cfeature.NaturalEarthFeature('cultural', 'urban_areas', '10m',
                    edgecolor='face',
                    facecolor="red",#cfeature.COLORS['water'],
                    zorder=0)
            ax.add_feature(rivers_10m)
            ax.add_feature(lake_10m)
            ax.add_feature(urban_10m)
        ax.add_feature(cfeature.BORDERS)
        #if self.name !="europe":
         #   ax.add_feature(cfeature.LAKES)
          #  ax.add_feature(cfeature.COASTLINE)
           # ax.add_feature(cfeature.STATES)
            #ax.add_feature(cfeature.BORDERS)
        ax.set_extent([self.lon_start, self.lon_end, self.lat_start, self.lat_end], crs=ccrs.PlateCarree())  # Begrenzung auf Europa
        # Kasten am unteren Rand einfügen
        ax.annotate(f'{self.time}', xy=(0.02, 0.04), xycoords='axes fraction',
                    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round',edgecolor="black"),fontsize=14)

        # Weitere Informationen im Kasten hinzufügen (anpassen, wie benötigt)
        additional_info = "EUMETSAT SEVIRI IR10.8μm + VIS0.6μm"
        ax.annotate(additional_info, xy=(0.98, 0.04), xycoords='axes fraction', ha='right',
                    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round',edgecolor="black"),fontsize=14)

        # Lokales GeoTIFF-Bild laden (ersetzen Sie 'lokales_bild.tif' durch den Pfad zu Ihrem GeoTIFF-Bild)
        #local_image_path = 'baseimages/vis/'+self.time+'.tiff'

        # GeoTIFF-Bild mit Rasterio öffnen
        #with rasterio.open(local_image_path) as src:
         #   local_image = src.read(1)  # Annahme: Das Bild hat eine einzige Bande


        #cloud_brightness_threshold = 65

       # cloud_mask = np.where(local_image > cloud_brightness_threshold, 1, 0)
        print('Projecting and plotting image...')
        # Erstelle das Ausgabebild, in dem nur die Wolken weiß sind (0 bleiben schwarz)
        output_image_ir = image_brigtness(cloud_brightness_threshold=65,time=self.time,visible=False)#,region=self.region)#np.where(cloud_mask == 1, local_image + 10, np.nan)
        output_image_vis =image_brigtness(cloud_brightness_threshold=65,time=self.time,visible=True)#,region=self.region) #np.where(cloud_mask == 1, local_image + 10, np.nan)


        extent = (-70, 70, 24, 72) #self.bbox
        ax.imshow(output_image_ir, origin='upper', transform=ccrs.PlateCarree(), extent=extent, alpha=0.6,cmap='gray', vmin=0,vmax=255)

        ax.imshow(output_image_vis, origin='upper', transform=ccrs.PlateCarree(), extent=extent, alpha=0.6,cmap='gray', vmin=0,vmax=255)


        if self.radar:
            print("start radar")
            """
            with rasterio.open("baseimages/radar/geotiff_n.tiff") as src:
                output_image_radar  = src.read(1)
                extent = src.bounds  # Die Bounding Box der GeoTIFF-Datei

                # Transformiere die Extents in geografische Koordinaten
                from rasterio.warp import transform_bounds
                left, bottom, right, top = transform_bounds(src.crs, {'init': 'epsg:4326'}, extent.left, extent.bottom, extent.right, extent.top)

                #left = 1.435612143
                #bottom= 45.68358331
                #right= 16.60186543
                #top= 55.86584289

                print(left,bottom,right,top)

                            # Erstelle eine Maske, um Werte von 0 (kein Niederschlag) zu maskieren
                mask_array = np.where(output_image_radar == 0, 1, 0)  # Hier gehen wir davon aus, dass 0 keine Niederschlagsdaten bedeutet
                  # Finde die Konturen der Maske
                contours = ndimage.find_objects(ndimage.label(output_image_radar)[0])
                # Wende die Maske auf das Raster an, um lila Flächen transparent zu machen
                mask_with_contours = np.zeros_like(output_image_radar)
                output_image_radar = np.ma.masked_array(output_image_radar, mask=mask_array)


                    # Füge eine separate Ebene hinzu, um die Konturen zu zeichnen (z.B., schwarze Konturen)

                for contour in contours:
                    if contour is not None:
                        mask_with_contours[contour] = 1
                # Koordinatentransformation, um die Koordinaten in Pixel zu übersetzen
                transform = src.transform#https://maps.dwd.de/geoserver/dwd/ows?SERVICE=WMS&service=WMS&request=GetLegendGraphic&format=image%2Fpng&layer=RV-Produkt

            ds1 = wrl.io.open_raster("baseimages/radar/geotiff_n.tiff")
            #data1, xy1, proj1 = wrl.georef.extract_raster_dataset(ds1, nodata=-9999.0)


            #ax.pcolormesh(xy1[..., 0], xy1[..., 1], data1[0], transform=ccrs.PlateCarree())#, extent=extent) 
            #ax.pcolormesh(filtered_xy[:, 0].reshape(filtered_data.shape), filtered_xy[:, 1].reshape(filtered_data.shape), filtered_data, cmap='gray', vmin=0, vmax=255, transform=ccrs.PlateCarree())

            #output_image_radar =image_brigtness(cloud_brightness_threshold=5,time=self.time,radar=True)
            # Definiere die Farben und Intervalle
            colors = [
                (0, 'lightblue', 0),  # Vollständig transparent
                (0.1, 'lightblue', 1),
                (0.2, 'blue', 1),
                (0.4, 'darkgreen', 1),
                (1.0, 'lightgreen', 1),
                (2.0, 'yellowgreen', 1),
                (3.0, 'brown', 1),
                (5.0, 'yellow', 1),
                (7.5, 'gold', 1),
                (10.0, 'orange', 1),
                (15.0, 'orangered', 1),
                (30.0, 'red', 1),
                (45.0, 'pink', 1),
                (75.0, 'pink', 1),
                (100.0, 'purple', 1),
                (150.0, 'blue', 1),
                (np.inf, 'blue', 1)  # Vollständig undurchsichtig
            ]
            #values = [0, 0.1, 0.2, 0.4, 1.0, 2.0, 3.0, 5.0, 7.5, 10.0, 15.0, 30.0, 45.0, 75.0, 100.0, 150.0]
            values = [0,7,19,28,37,46,55]
            #colorss = [
           #     'lightblue', 'lightblue', 'blue', 'darkgreen',
           #     'lightgreen', 'yellowgreen', 'brown', 'yellow',
           #     'gold', 'orange', 'orangered', 'red', 'pink', 'pink', 'purple', 'blue'
           # ]
            colorss = [ "green", "turquoise", "lightblue","blue","darkblue","purple","red"]
            # Erstelle die benutzerdefinierte Colormap
            # Normalisiere die Werte auf den Bereich von 0 bis 1
            normalized_values = [v / 55.0 for v in values]

            # Erstelle die benutzerdefinierte Colormap
            color_list = list(zip(normalized_values, colorss))

            custom_cmap = LinearSegmentedColormap.from_list('custom_colormap', color_list)

            #custom_cmap = LinearSegmentedColormap.from_list('custom_colormap', colors)
            ax.imshow(output_image_radar, origin='upper', transform=ccrs.PlateCarree(),extent=(left, right, bottom, top),cmap=custom_cmap)#,extent=(5.9, 13.1,48.3, 54))#,extent=(extent.left, extent.right, extent.bottom, extent.top))#, extent=extent)#, cmap='gray', vmin=0,vmax=255)
            #ax.imshow(mask_with_contours, origin='upper', transform=ccrs.PlateCarree(),extent=(left, right, bottom, top),cmap='gray', alpha=0.7)#,extent=(5.9, 13.1,48.3, 54))#,extent=(extent.left, extent.right, extent.bottom, extent.top))#, extent=extent)#, cmap='gray', vmin=0,vmax=255)
            """

            input_file = "radar/input/raa01-yw_10000-latest-dwd---bin"
            ds = wrl.io.open_radolan_dataset(input_file)
            # print the xarray dataset
            print(ds)
            #ax.plot(ds.YW,cmap="viridis", transform=ccrs.PlateCarree())
            #ds["YW"].plot.contourf(ax=ax, transform=ccrs.PlateCarree(), levels=21)
            #ax.contourf(ds.YW,transform=ccrs.PlateCarree(),levels=21,extent=extent,)
            ax.contourf(ds.YW.where(ds.YW != 0, np.nan), transform=ccrs.PlateCarree(),extent=[1.435612143, 16.60186543, 45.68358331, 55.86584289],cmap="jet_r")


            print("radar finished")
        print("start saving")
        ax.set_frame_on(False)
        plt.tight_layout()
        #
        # plt.show()
        plt.savefig(self.export_path+self.name+'/'+self.name+'_'+self.time+'.png', dpi=150)

        return


def request_sats(timestart,timeend,time_file,visible=False, bbox=(-70, 24, 70, 72),region="europe", sizemulti=5):
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
    #

    format_option = 'image/geotiff'

    payload = {
        'layers': [target_layer],
        'styles': '',
        'format': format_option,
        'crs': 'EPSG:4326',
        # 'bbox'   : (-77.7699966430664, -77.7699966430664, 77.7699966430664, 77.7699966430664),
        # 'bbox'   : (-45,35,45,62),
        'bbox': bbox,#(-70, 24, 70, 72),
        'size': (sizemulti*945, sizemulti*945),
        #'time': '2023-08-16T22:00:00.000Z/2023-08-16T22:00:00.000Z'
        'time': timestart+"/"+timeend
    }

    wms = WebMapService(service_url, auth=Authentication(verify=False))
    img = wms.getmap(**payload)
    Image(img.read())
    with open("baseimages/"+file_loc+"/"+time_file+'.tiff', 'wb') as f: #+region+"/"
        f.write(img.read())
    return


def singlemaps(export_path):
    datetime_obj = datetime(2023, 9, 1, 12, 0, 0)  # Hier setzen Sie Ihr eigenes datetime-Objekt ein

    times = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    time  = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    #request_sats(times,times,time,visible=True,region="germany",sizemulti=2)
    #request_sats(times, times, time, visible=False,region="germany",sizemulti=2)

    print("starting europe")
    europe = satelite_image( 35, 65,-45, 45,time,"europe",export_path=export_path,radar=True)

    europe.remap()

    print("starting germany")
    #germany = satelite_image( 47, 55,5, 15,time,"germany",export_path=export_path)#,bbox=(0,20,40,60), region="germany")#,radar=True)
    germany = satelite_image( 46.3, 56,1.9, 19.1,time,"germany",export_path=export_path,radar=True)
    germany.remap()

    print("starting lower_saxony")
    lower_saxony = satelite_image( 51.2, 53.9,5.2, 13.,time,"lower_saxony",export_path=export_path,radar=True)

    lower_saxony.remap()


    print("starting hannover")
    hannover = satelite_image(52.117469,52.604716,9,10.5,time,"hannover",export_path=export_path,radar=True)

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





def singlemaps_pool(export_path):
    with Pool() as pool:
        pool.map(varrequest, number)

    return

#multimap()
#radarrconvert()
#radarrconvertrio()
#request_sats("2023-09-01T12:00:00.000Z","2023-09-01T12:00:00.000Z","2023-09-01 12:00:00",visible=True)
start_time = time.time()
singlemaps(export_path= "/mnt/nvmente/CODE/imuk/database/output/satelite/")
print("--- %s seconds ---" % (time.time() - start_time))


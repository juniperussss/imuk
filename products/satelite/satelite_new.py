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

def image_brigtness(cloud_brightness_threshold,T=0,visible=False,radar=False): #,region

    if visible:
        local_image_path = 'oldcwd+"/database/input/satelite/vis/'  +"latest_T-"+str(T) + '.tiff' #+ region +'/'+ 
    elif radar:
        local_image_path = 'baseimages/radar/geotiff_n.tiff'
    else:
        local_image_path = 'oldcwd+"/database/input/satelite/ir/'  +"latest_T-"+str(T) +'.tiff'

    # GeoTIFF-Bild mit Rasterio öffnen
    with rasterio.open(local_image_path) as src:
        local_image = src.read(1)  # Annahme: Das Bild hat eine einzige Bande

    #cloud_brightness_threshold = 65

    cloud_mask = np.where(local_image > cloud_brightness_threshold, 1, 0)
    output=np.where(cloud_mask == 1, local_image + 10, np.nan)
    return output


def satimage(name= "europe", T=0, radar=True, exportpath="",coords=[], time=datetime.now()):
        
        lat_start = coords[0]
        lat_end = coords[1]
        lon_start = coords[2]
        lon_end = coords[3]
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
        if name =="lower_saxony":
            ax.add_feature(cfeature.STATES)
        elif name == "hannover":
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
        ax.set_extent([lon_start, lon_end, lat_start, lat_end], crs=ccrs.PlateCarree())  # Begrenzung auf Europa
        ax.annotate(f'{time.strftime('%Y-%m-%d %H:%M:%S')}', xy=(0.02, 0.04), xycoords='axes fraction',
                    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round',edgecolor="black"),fontsize=14)
        additional_info = "EUMETSAT SEVIRI IR10.8μm + VIS0.6μm"
        ax.annotate(additional_info, xy=(0.98, 0.04), xycoords='axes fraction', ha='right',
                    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round',edgecolor="black"),fontsize=14)
        print('Projecting and plotting image...')
        # Erstelle das Ausgabebild, in dem nur die Wolken weiß sind (0 bleiben schwarz)
        output_image_ir = image_brigtness(cloud_brightness_threshold=65,T=str(T),visible=False)#,region=self.region)#np.where(cloud_mask == 1, local_image + 10, np.nan)
        output_image_vis =image_brigtness(cloud_brightness_threshold=65,T=str(T),visible=True)#,region=self.region) #np.where(cloud_mask == 1, local_image + 10, np.nan)


        extent = (-70, 70, 24, 72) #self.bbox
        ax.imshow(output_image_ir, origin='upper', transform=ccrs.PlateCarree(), extent=extent, alpha=0.6,cmap='gray', vmin=0,vmax=255)

        ax.imshow(output_image_vis, origin='upper', transform=ccrs.PlateCarree(), extent=extent, alpha=0.6,cmap='gray', vmin=0,vmax=255)
        if radar:
            print("start radar")
            input_file = oldcwd+"/database/input/radar/"+"radar_latest_T-"+str(T)
            ds = wrl.io.open_radolan_dataset(input_file)
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
        plt.savefig(export_path+name+'/'+name+'_latest_T-'+str(T)+'.png', dpi=150)

        
        return


coords = [52.117469,52.604716,9,10.5]
satimage(export_path= "/mnt/nvmente/CODE/imuk/database/output/satelite/",coords=coords)
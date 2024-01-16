import os, sys
import warnings
from IPython.core.display import HTML
from IPython.display import Image
from owslib.wms import WebMapService
from owslib.util import Authentication
from skimage import io
import requests
from datetime import datetime, timedelta

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
#import gdal

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1, 1, 1,projection=ccrs.PlateCarree()) # projection=ccrs.LambertConformal(central_longitude=10))
ax.coastlines()
ax.add_feature(cfeature.LAND, facecolor='darkgreen')
ax.add_feature(cfeature.OCEAN, facecolor='navy')

#ax.add_feature(cfeature.LAKES)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.BORDERS)
#ax.set_extent([5, 15,47, 55], crs=ccrs.PlateCarree())
extent = (5, 15,47, 55)
print("start radar")
with rasterio.open("../baseimages/radar/geotiff.tif",driver='GTiff',) as src:
    output_image_radar = src.read(1)
    #cloud_mask = np.where(output_image_radar > 1, 1, 0)
    cloud_masker = np.where(output_image_radar < 254, 1, 0)
    #output_image_radar=np.where(cloud_mask == 1, output_image_radar, np.nan)
    output_image_radar=np.where(cloud_masker == 1, output_image_radar + 10, np.nan)


#dataset = rasterio.open("../baseimages/radar/geotiff.tif")
#print(dataset.bounds)
    # output_image_radar =image_brigtness(cloud_brightness_threshold=5,time=self.time,radar=True)
ax.imshow(output_image_radar, origin='upper',extent=extent,transform=ccrs.PlateCarree())#, vmin=0, vmax=255)

ax.set_frame_on(False)
plt.tight_layout()
plt.savefig('test.png', dpi=300)
import os
import wradlib as wrl
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
#import gdal

import cartopy.crs as ccrs

map_proj = ccrs.Stereographic(
    true_scale_latitude=60.0, central_latitude=90.0, central_longitude=10.0
)
# DOESNT WORK WITH CONDA ATM USE PIP
warnings.filterwarnings("ignore")
#try:
 #   get_ipython().run_line_magic("matplotlib inline")
#except:
plt.ion()
import numpy as np
import xarray as xr
import pandas as pd

#data, metadata = wrl.io.read_radolan_composite("DE1200_RV2309130955_000")
#print(metadata)
#data.nodatamask.plot()
#plt.show()

# load radolan files
#rw_filename = wrl.util.get_wradlib_data_file(
 #   "raa01-rw_10000-latest-dwd---bin.bz2"
#)
ds, metads = wrl.io.read_radolan_composite("DE1200_RV2309130955_000",fillmissing=True)
rwdata, rwattrs = wrl.io.read_radolan_composite("raa01-rw_10000-latest-dwd---bin")
print("RW Attributes:", rwattrs)

# do some masking
sec = rwattrs["secondary"]
rwdata.flat[sec] = -9999
rwdata = np.ma.masked_equal(rwdata, -9999)
#wrl.show_versions()
# Get coordinates
radolan_grid_xy = wrl.georef.get_radolan_grid()
x = radolan_grid_xy[:, :, 0]
y = radolan_grid_xy[:, :, 1]


# plot function
plt.pcolormesh(x, y, rwdata, cmap="viridis")
cb = plt.colorbar(shrink=0.75)
cb.set_label("mm * h-1")
plt.title("RADOLAN RW Product Polar Stereo \n" + rwattrs["datetime"].isoformat())
plt.grid(color="r")
plt.savefig("radolan_plot.png")
#plt.show()



#df = pd.DataFrame(ds)
#dx = xr.DataArray(df)
#print(dx)
#sns.pointplot(df)
#plt.show()

ds = wrl.io.open_radolan_dataset("raa01-rw_10000-latest-dwd---bin")
ds = wrl.io.open_radolan_dataset("DE1200_RV2309130955_000")
ds.RV.to_netcdf("radolan.nc")

# print the xarray dataset
print(ds)
#ds.RV.plot()
#plt.savefig("radolan_plot2.png")

fig = plt.figure(figsize=(10, 8))
ds.RV.plot(subplot_kws=dict(projection=map_proj))
ax = plt.gca()
ax.gridlines(draw_labels=True, y_inline=False)
plt.show()

plt.savefig("radolan_plot2.png")

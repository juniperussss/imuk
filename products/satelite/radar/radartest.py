import os
import wradlib as wrl
import matplotlib.pyplot as plt
import warnings
import cartopy.crs as ccrs

import numpy as np
import xarray as xr



warnings.filterwarnings("ignore")

input_file = "products/satelite/radar/input/raa01-yw_10000-latest-dwd---bin"
ds = wrl.io.open_radolan_dataset(input_file)
# print the xarray dataset
print(ds)
plt.figure(dpi=150)
projection = ccrs.Mercator()

# Specify CRS, that will be used to tell the code, where should our data be plotted
crs = ccrs.PlateCarree()
ax = plt.axes(projection=projection, frameon=True)

# Draw gridlines in degrees over Mercator map
gl = ax.gridlines(crs=crs, draw_labels=True,
                  linewidth=.6, color='gray', alpha=0.5, linestyle='-.')
gl.xlabel_style = {"size" : 7}
gl.ylabel_style = {"size" : 7}

# To plot borders and coastlines, we can use cartopy feature
import cartopy.feature as cf
ax.add_feature(cf.COASTLINE.with_scale("50m"), lw=0.5)
ax.add_feature(cf.BORDERS.with_scale("50m"), lw=0.3)

# Now, we will specify extent of our map in minimum/maximum longitude/latitude
# Note that these values are specified in degrees of longitude and degrees of latitude
# However, we can specify them in any crs that we want, but we need to provide appropriate
# crs argument in ax.set_extent
lon_min = -20
lon_max = 45
lat_min = 34
lat_max = 60

# crs is PlateCarree -> we are explicitly telling axes, that we are creating bounds that are in degrees
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=crs)
#plt.title(f"Temperature anomaly over Europe in {original_data.valid_time.dt.strftime('%B %Y').values}")
#ds.YW.to_netcdf("radartest.nc")
#plt.pcolormesh(ds.YW, cmap="viridis")
#ds.YW.plot()
#ds.YW.plot(subplot_kws=dict(projection=ccrs.PlateCarree()))
ax.contourf(ds.YW.where(ds.YW != 0, np.nan), transform=ccrs.PlateCarree(),extent=[1.435612143, 16.60186543, 45.68358331, 55.86584289],cmap="jet_r")
plt.show()
#Placeholder
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pyproj
import cartopy.feature as cfeature


lon_start = -10
lon_end = 28
lat_start = 60
lat_end = 35

fig = plt.figure(figsize=(12.8,7.2))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal(
    central_longitude=10))  # ,central_latitude=52) ) #ccrs.Miller())#
pyproj.set_use_global_context()
#ax.coastlines()
#ax.LAKES()
ax.add_feature(cfeature.COASTLINE)
#ax.add_feature(cfeature.LAND)#, facecolor='darkgreen')
land_110m = cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                edgecolor='face',
                                facecolor="darkgreen",#cfeature.COLORS['land'],
                                zorder=0)
ax.add_feature(land_110m)


ocean_110m = cfeature.NaturalEarthFeature('physical', 'ocean', '50m',
                                edgecolor='face',
                                facecolor="navy",#cfeature.COLORS['water'],
                                zorder=0)
ax.add_feature(ocean_110m)

ax.set_extent([lon_start, lon_end, lat_start,lat_end], crs=ccrs.PlateCarree())  # Begrenzung auf Europa

plt.show()
Can you please try this script to run? If it works well, the problem stems from the definition of add_feature methods.

import os
import warnings
from datetime import datetime, timedelta
from pyproj.crs import CRS
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import rasterio
from rasterio.plot import show
import ndimage
import wradlib as wrl
from matplotlib.colors import LinearSegmentedColormap

# Define the function to create the Cartopy map with lakes and rivers
def create_map_with_lakes_rivers(time, name):
    # Create a figure and axis for the map
    fig = plt.figure(figsize=(12.8, 7.2))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal(central_longitude=10))

    # Add land and coastline features
    ax.add_feature(cfeature.COASTLINE)
    land_110m = cfeature.NaturalEarthFeature('physical', 'land', '110m', edgecolor='face', facecolor="darkgreen", zorder=0)
    ax.add_feature(land_110m)
    ocean_110m = cfeature.NaturalEarthFeature('physical', 'ocean', '110m', edgecolor='face', facecolor="navy", zorder=0)
    ax.add_feature(ocean_110m)

    # Add lakes and rivers (customize as needed)
    ax.add_feature(cfeature.LAKES, facecolor='none', edgecolor='blue')
    ax.add_feature(cfeature.RIVERS, edgecolor='blue')

    # Set the map's extent
    ax.set_extent([lon_start, lon_end, lat_start, lat_end], crs=ccrs.PlateCarree())

    # Additional annotations or information can be added here

    # Load and process the radar image
    # ...

    # Plot the radar image on the map
    # ...

    # Save the map as an image
    ax.set_frame_on(False)
    plt.tight_layout()
    plt.savefig(f'{name}/{name}_{time}.png', dpi=300)

# Define your region of interest and time
lat_start = 51.2
lat_end = 53.9
lon_start = 5.2
lon_end = 13.0
time = "2023-09-01 12:00:00"
name = "lower_saxony"

# Call the function to create the map with lakes and rivers
create_map_with_lakes_rivers(time, name)


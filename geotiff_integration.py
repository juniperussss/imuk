pip install metpy matplotlib

import rasterio

# The crucial thing here is in the following:

# Open the Geotiff file
with rasterio.open('your_geotiff_file.tif') as dataset:
    # Access metadata
    print(dataset.meta)

    # Read the data as a NumPy array
    data = dataset.read(1)  # Replace '1' with the band number you want to read

import metpy.calc as mpcalc
from metpy.units import units
import numpy as np

# Convert temperature data to Celsius
temperature_data = data * units('K')
temperature_data_celsius = mpcalc.temperature_from_isentropic(1000 * units.hPa, 1000 * units.hPa, temperature_data)

# Create a contour plot
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 8))
plt.contourf(dataset.bounds.right, dataset.bounds.top, temperature_data_celsius.magnitude, cmap='coolwarm')
plt.colorbar(label='Temperature (°C)')
plt.title('Temperature from Geotiff Data')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid()
plt.show()

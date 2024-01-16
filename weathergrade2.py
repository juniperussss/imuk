import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from metpy.plots import simple_layout, StationPlot

# Sample data for station points (longitude, latitude, weather condition, importance grade)
stations = [
    {"lon": -75.1652, "lat": 39.9526, "weather": "cloud", "grade": 2},  # Philadelphia (cloudy)
    {"lon": -122.4194, "lat": 37.7749, "weather": "rain", "grade": 3},   # San Francisco (rainy)
    {"lon": -74.006, "lat": 40.7128, "weather": "fog", "grade": 1},      # New York (foggy)
    {"lon": 10.0000, "lat": 53.5500, "weather": "rain", "grade": 2},     # Hamburg (rainy)
    {"lon": 10.0001, "lat": 53.5501, "weather": "cloud", "grade": 1},    # Hamburg (cloudy)
    # Add more station points here
]

# Meteorological symbols
meteorological_symbols = {
    "cloud": "☁",
    "rain": "🌧",
    "fog": "— — —",  # Three horizontal lines represent fog
    # Add more weather symbols here
}

# Create the map
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax = simple_layout(ax, extent=[-130, 20, 20, 60])

# Create a station plot
sp = StationPlot(ax, [station["lon"] for station in stations], 
                 [station["lat"] for station in stations],
                 transform=ccrs.PlateCarree(), fontsize=12)

# Plot station points and weather symbols
for station in stations:
    lon, lat, weather, grade = station["lon"], station["lat"], station["weather"], station["grade"]
    symbol = meteorological_symbols.get(weather, "?")
    sp.plot_symbol('C', symbol, weather, fontsize=12 + grade * 2, zorder=5)

# Set the map extent and show the plot
ax.set_extent([-130, 20, 20, 60], crs=ccrs.PlateCarree())
plt.show()

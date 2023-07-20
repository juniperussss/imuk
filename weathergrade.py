import matplotlib.pyplot as plt
import cartopy.crs as ccrs

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

# Function to plot weather symbols based on weather condition and importance grade
def plot_weather_symbol(ax, lon, lat, weather, grade):
    if weather in meteorological_symbols:
        symbol = meteorological_symbols[weather]
        ax.text(lon, lat, symbol, fontsize=12 + grade * 2, ha="center", va="center")
    else:
        ax.text(lon, lat, "?", fontsize=12 + grade * 2, ha="center", va="center")  # Unknown weather

# Create the map
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Add coastlines and gridlines
ax.coastlines()
ax.gridlines()

# Sort stations based on importance grade in descending order
stations.sort(key=lambda x: x["grade"], reverse=True)

# Plot station points and weather symbols, avoiding overlapping symbols
station_positions = set()  # To keep track of already used positions
for station in stations:
    lon, lat, weather, grade = station["lon"], station["lat"], station["weather"], station["grade"]
    pos = (lon, lat)

    # Check if the position is already plotted; if not, plot the weather symbol
    if pos not in station_positions:
        ax.plot(lon, lat, marker="o", markersize=10, color="red", transform=ccrs.Geodetic())
        plot_weather_symbol(ax, lon, lat, weather, grade)
        station_positions.add(pos)

# Set the map extent and show the plot
ax.set_extent([-130, 20, 20, 60], crs=ccrs.PlateCarree())
plt.show()

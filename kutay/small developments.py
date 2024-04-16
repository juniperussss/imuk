ax.add_feature(cfeature.LAND.with_scale('50m'), facecolor='lightgray')  # Added scale and color
ax.add_feature(cfeature.OCEAN.with_scale('50m'), facecolor='lightblue')  # Added scale and color
ax.add_feature(cfeature.LAKES.with_scale('50m'), facecolor='lightblue')  # Added scale and color
ax.add_feature(cfeature.COASTLINE.with_scale('50m'))  # Added scale
ax.add_feature(cfeature.STATES.with_scale('50m'))  # Added scale
ax.add_feature(cfeature.BORDERS.with_scale('50m'))  # Added scale


# Coordinates for Hannover, Germany
hannover_lat = 52.5200
hannover_lon = 9.2057

# Convert coordinates to map projection
hannover_x, hannover_y = m(hannover_lon, hannover_lat)

# Plot Hannover as a red dot
m.plot(hannover_x, hannover_y, 'ro', markersize=6, label='Hannover')
plt.show()
from matplotlib.colors import LinearSegmentedColormap

def create_custom_colormap():
    colors = [
        (0, 'lightblue', 0),
        (0.1, 'lightblue', 1),
        (0.2, 'blue', 1),
        (0.4, 'darkgreen', 1),
        (1.0, 'lightgreen', 1),
        # ... Add more color stops ...
        (np.inf, 'blue', 1)
    ]

    values = [0, 0.1, 0.2, 0.4, 1.0, np.inf]
    custom_cmap = LinearSegmentedColormap.from_list('custom_colormap', colors, N=256)
    return custom_cmap

# Usage example:
# custom_cmap = create_custom_colormap()
# plt.imshow(data, cmap=custom_cmap, vmin=0, vmax=255)



IN ADDITION TO THESE:

Common colorbars for radar reflectivity include:

"cmap='viridis'": Viridis is a perceptually uniform color map that goes from dark blue (low reflectivity) to yellow (high reflectivity). It's a good choice for visualizing radar reflectivity because it avoids misleading color gradients.

"cmap='cividis'": Similar to viridis, cividis is another perceptually uniform color map that may be suitable for radar reflectivity.

"cmap='rainbow'": The rainbow color map is widely recognized, but it's not perceptually uniform. It's important to be cautious when using rainbow color maps as they can introduce artifacts.


MY RECOMMENDATIONS:

If we use dataset of:

1. Reflectivity (dBZ): A blue-to-red colorbar, where light blue represents light precipitation, green represents moderate precipitation, and red represents heavy precipitation. This color scheme is intuitive and widely recognized in meteorology.

2. Velocity (m/s): A color diverging from blue to red, where blue represents motion toward the radar (inflow) and red represents motion away from the radar (outflow). This color scheme helps identify wind patterns and storm rotation.

3. Precipitation Rate (mm/hr): A color scale that spans from light blue (low precipitation rate) to dark blue (moderate precipitation rate) and green to red (heavy precipitation rate). This provides a clear representation of precipitation intensity.

4. Differential Reflectivity (dB): A color diverging from blue to red, with zero as the reference point (white or gray). Blue represents regions where precipitation is primarily rain, and red represents regions where precipitation is primarily snow or ice.

5. Correlation Coefficient: A color scale that spans from blue to red, with values close to 1 (high correlation) in blue and values close to 0 (low correlation) in red.
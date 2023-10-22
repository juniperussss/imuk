# MARKING OF CITY CENTER HANNOVER

import matplotlib.pyplot as plt

def mark_city_center():
    hannover_city_lat, hannover_city_lon = 52.3759, 9.7320

    # Create a scatter plot to mark the city center
    plt.scatter(hannover_city_lon, hannover_city_lat, color='blue', marker='o', label='Hannover City Center')

    # Customize the plot
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(linestyle='--', alpha=0.5)

    # Add a legend
    plt.legend(loc='upper left')
    plt.tight_layout()

    # Show the plot
    plt.show()

mark_city_center()

# ADDING CIRCLES SURROUNDING AREA

import matplotlib.pyplot as plt
import numpy as np

def fancy_radar_visualization():
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))

    # Define the coordinates of Hannover
    hannover_city_lat, hannover_city_lon = 52.3759, 9.7320

    # Create concentric circles with colors and titles
    radii = np.arange(50, 301, 50)
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'cyan', 'magenta']
    titles = ['50 km', '100 km', '150 km', '200 km', '250 km', '300 km', '350 km']

    for radius, color, title in zip(radii, colors, titles):
        circle = plt.Circle((hannover_city_lon, hannover_city_lat), radius, fill=False, color=color, label=title)
        ax.add_patch(circle)

    # Customize the plot

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(linestyle='--', alpha=0.5)

    # Add a legend
    plt.legend(loc='upper left', title='Circle Radii')

    # Show the plot
    plt.axis('equal')  # Equal aspect ratio
    plt.tight_layout()
    plt.show()

fancy_radar_visualization()


import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from metpy.calc import reduce_point_density
from metpy.cbook import get_test_data
from metpy.io import metar
from metpy.plots import add_metpy_logo, current_weather, sky_cover, StationPlot,pressure_tendency
import argparse
#file ="/home/alex/code/imuk/ressources/Data/metarsupp.csv"

path_origin = "/home/alex/code/imuk"


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('inputpath')  # 350
    parser.add_argument('outputpath')  # 350
    args = parser.parse_args()
    path_origin = args.inputpath
    output = args.outputpath#'database/input/icon/'
        # Set up the map projection
    proj = ccrs.LambertConformal(central_longitude=10, central_latitude=52,
                                standard_parallels=[35])

    data = pd.read_csv(path_origin+"/ressources/Data/metarsupp.csv")

    # Use the Cartopy map projection to transform station locations to the map and
    # then refine the number of stations plotted by setting a 300km radius
    point_locs = proj.transform_points(ccrs.PlateCarree(), data['lon'].values,
                                    data['lat'].values)
    data = data[reduce_point_density(point_locs, 40000.)]


    print(data["pressure3h_change"].astype(int))
    # Change the DPI of the resulting figure. Higher DPI drastically improves the
    # look of the text rendering.
    plt.rcParams['savefig.dpi'] = 600

    # Create the figure and an axes set to the projection.
    fig = plt.figure(figsize=(9, 8))
    #add_metpy_logo(fig, 1100, 300, size='large')
    ax = fig.add_subplot(1, 1, 1, projection=proj)

    # Add some various map elements to the plot to make it recognizable.
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.LAKES)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.STATES)
    ax.add_feature(cfeature.BORDERS)

    # Set plot bounds
    ax.set_extent((-15, 50, 30, 68))



    stationplot = StationPlot(ax, data['lon'].values, data['lat'].values,
                            clip_on=True, transform=ccrs.PlateCarree(), fontsize=3)

    # Plot the temperature and dew point to the upper and lower left, respectively, of
    # the center point. Each one uses a different color.
    stationplot.plot_parameter('NW', data['temperature'].values, color='red')
    stationplot.plot_parameter('SW', data['dewpoint'].values,
                            color='darkgreen')

    # A more complex example uses a custom formatter to control how the sea-level pressure
    # values are plotted. This uses the standard trailing 3-digits of the pressure value
    # in tenths of millibars.
    stationplot.plot_parameter('NE', data['pressure'].values,
                            formatter=lambda v: format(10 * v, '.0f')[-3:])


    # Plot the cloud cover symbols in the center location. This uses the codes made above and
    # uses the `sky_cover` mapper to convert these values to font codes for the
    # weather symbol font.
    data['cloudcover'] = data['cloudcover'].fillna(0)
    data['cloudcover'] = data['cloudcover'].astype(int)

    stationplot.plot_symbol('C', data['cloudcover'].values, sky_cover)
    #stationplot.plot_symbol('SE', data['pressure3h_change'].values.astype(int), pressure_tendency)


    # Split Wind in u and v components

    data["u"] = data["windspeed"] * np.cos(np.deg2rad( data["winddir"]))
    data ["v"] = data["windspeed"] * np.sin(np.deg2rad( data["winddir"]))

    stationplot.plot_barb(data['u'].values, data['v'].values)


    data['weather'] = data['weather'].fillna(0)
    data['weather'] = data['weather'].astype(int)

    # Same this time, but plot current weather to the left of center, using the
    # `current_weather` mapper to convert symbols to the right glyphs.
    stationplot.plot_symbol('W', data['weather'].values, current_weather)

    # Also plot the actual text of the station id. Instead of cardinal directions,
    # plot further out by specifying a location of 2 increments in x and 0 in y.
    #stationplot.plot_text((2, 0), data['station'].values)
    plt.tight_layout()
    plt.savefig(output+"/stationmap_metpy_2.png")

    #plt.show()

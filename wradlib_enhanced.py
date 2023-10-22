def radarrconvert_wradlib(filename):
    import wradlib as wrl
    import numpy as np
    import warnings
    warnings.filterwarnings('ignore')

    data_raw = wrl.io.open_radolan_dataset(filename).RV
    proj_osr = wrl.georef.create_osr("dwd-radolan")
    xy_raw = wrl.georef.get_radolan_grid(1200, 1100)

    data, xy = wrl.georef.set_raster_origin(data_raw, xy_raw, 'upper')
    data = np.stack((data, data + 100, data + 1000), axis=0)

    ds = wrl.georef.create_raster_dataset(data, xy, crs=proj_osr)
    wrl.io.write_raster_dataset("baseimages/radar/geotiff_n.tiff", ds, driver='GTiff')


def plot_radar_data(data, extent, title):
    import matplotlib.pyplot as plt
    import wradlib as wrl

    fig, ax = plt.subplots(figsize=(10, 8))
    wrl.vis.plot_ppi(data, ax=ax, r=extent[2], title=title, cmap='viridis')
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    plt.show()

# Usage example:
# plot_radar_data(data, extent=(-70, 70, 24, 72), title='Radar Data')


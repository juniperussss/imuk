import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import rasterio
from rasterio.plot import show
import numpy as np
import cartopy.feature as cfeature


def main():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal(central_longitude=0,central_latitude=52) )
    ax.coastlines()
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.set_extent([-45, 45, 32, 62], crs=ccrs.PlateCarree())  # Begrenzung auf Europa

    # Lokales GeoTIFF-Bild laden (ersetzen Sie 'lokales_bild.tif' durch den Pfad zu Ihrem GeoTIFF-Bild)
    local_image_path = 'output_image.tiff'

    # GeoTIFF-Bild mit Rasterio öffnen
    with rasterio.open(local_image_path) as src:
        local_image = src.read(1)  # Annahme: Das Bild hat eine einzige Bande


    print('Projecting and plotting image...')
    extent = (-6500000, 5500000, -5500000, 6000000)
    #extent = (-3000000,3000000,-2000000,2000000)
    #extent =(-45,45,38,62)
   # masked_image = np.where(local_image < 256)

   # cmap = plt.cm.gray
    #cmap.set_bad((0, 0, 0, 0))  # Setzen Sie den Alphawert für die transparenten Bereiche

    ax.imshow(local_image,origin='upper',extent=extent, transform=ccrs.Geostationary(central_longitude=0), cmap='gray')#,  vmin=0, vmax=255)
    plt.show()


if __name__ == '__main__':
    main()

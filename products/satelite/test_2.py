import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import rasterio
from rasterio.plot import show
import numpy as np
import cartopy.feature as cfeature


def main():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal(central_longitude=10))#,central_latitude=52) ) #ccrs.Miller())#
    ax.coastlines()
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.set_extent([-45, 45, 35, 65], crs=ccrs.PlateCarree())  # Begrenzung auf Europa

    # Lokales GeoTIFF-Bild laden (ersetzen Sie 'lokales_bild.tif' durch den Pfad zu Ihrem GeoTIFF-Bild)
    local_image_path = 'cut.tiff'

    # GeoTIFF-Bild mit Rasterio öffnen
    with rasterio.open(local_image_path) as src:
        local_image = src.read(1)  # Annahme: Das Bild hat eine einzige Bande


    print('Projecting and plotting image...')
    #extent = (-6500000, 5500000, -5500000, 6000000)
    #extent = (-3000000,3000000,-2000000,2000000)

    #extent =(-45,45,35,62)
    extent =(-70,70,24,72)
   # masked_image = np.where(local_image < 256)

   # cmap = plt.cm.gray
    #cmap.set_bad((0, 0, 0, 0))  # Setzen Sie den Alphawert für die transparenten Bereiche

    ax.imshow(local_image,origin='upper', transform=ccrs.PlateCarree(), cmap='gray',extent=extent,alpha=0.5)#,  vmin=0, vmax=255)
    # Berechne den dpi-Wert für die gewünschte Auflösung
    auflösung_breite = 1920
    auflösung_höhe = 1080
    zoll_pro_dpi = 1 / 80  # Standardmäßig etwa 80 dpi pro Zoll
    dpi = max(auflösung_breite / (zoll_pro_dpi * plt.rcParams['figure.figsize'][0]),
              auflösung_höhe / (zoll_pro_dpi * plt.rcParams['figure.figsize'][1]))

    plt.savefig('SAT_TEST.png',dpi=600)
    #plt.show()


if __name__ == '__main__':
    main()

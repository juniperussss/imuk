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
    ax.add_feature(cfeature.LAND, facecolor='darkgreen')
    ax.add_feature(cfeature.OCEAN, facecolor='navy')
    ax.add_feature(cfeature.STATES)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAKES)
    ax.add_feature(cfeature.RIVERS)
    ax.add_feature(cfeature.COASTLINE)
    river_50m = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '50m',
                                            facecolor='navy')
    #ax.add_feature(river_50m)
    #ax.set_extent([-45, 45, 35, 65], crs=ccrs.PlateCarree())  # Begrenzung auf Europa
    #ax.set_extent([6.2, 11.6, 51.3, 54.8], crs=ccrs.PlateCarree())  # Begrenzung auf Niedersachsen
    ax.set_extent([9.140625,10.357361,52.117469,52.604716], crs=ccrs.PlateCarree())  # Begrenzung auf Hannover


    # Lokales GeoTIFF-Bild laden (ersetzen Sie 'lokales_bild.tif' durch den Pfad zu Ihrem GeoTIFF-Bild)
    local_image_path = '../cut.tiff'

    # GeoTIFF-Bild mit Rasterio öffnen
    with rasterio.open(local_image_path) as src:
        local_image = src.read(1)  # Annahme: Das Bild hat eine einzige Bande

        # Helligkeitsschwelle festlegen


    print('Projecting and plotting image...')
    #extent = (-70, 70, 24, 72)
    #extent = (5684617.92140348,2639478.825283233 , -28777388.895850692,4580173.536020188)
    # Erstelle die Transparenz für das Bild
    transparent_local_image = np.repeat(local_image[:, :, np.newaxis], 3, axis=2)

    #transparent_local_image[:, :, 3] = alpha_mask  # Alphakanal hinzufügen

    #print('Projecting and plotting image...')
    #extent = (-6500000, 5500000, -5500000, 6000000)
    #extent = (-3000000,3000000,-2000000,2000000)

    #extent =(-45,45,35,62)
    extent =(-70,70,24,72)
   # masked_image = np.where(local_image < 256)

   # cmap = plt.cm.gray
    #cmap.set_bad((0, 0, 0, 0))  # Setzen Sie den Alphawert für die transparenten Bereiche
    cloud_brightness_threshold = 65

    # Erstelle eine Maske für die Wolken (alle Werte über der Helligkeitsschwelle werden zu 1)
    # Erstelle eine Maske für die Wolken (alle Werte über der Helligkeitsschwelle werden zu 1)
    cloud_mask = np.where(local_image > cloud_brightness_threshold, 1, 0)

    # Erstelle das Ausgabebild, in dem nur die Wolken weiß sind (0 bleiben schwarz)
    output_image = np.where(cloud_mask == 1, local_image+10, np.nan)

    # Setze alle nicht-wolkenhaften Bereiche auf transparent
    #ax.imshow(output_image, origin='upper', transform=ccrs.PlateCarree(), extent=extent, cmap='gray')

    #ax.imshow(output_image, origin='upper', transform=ccrs.PlateCarree(), extent=extent, cmap='gray', vmin=0, vmax=255)

    #ax.imshow(transparent_local_image,origin='upper', transform=ccrs.PlateCarree(),extent=extent)#,alpha=0.5)#,  vmin=0, vmax=255)
   # ax.imshow(local_image, origin='upper', transform=ccrs.PlateCarree(), extent=extent, cmap='gray')
    #ax.imshow(alpha_mask, origin='upper', transform=ccrs.PlateCarree(), extent=extent, cmap='gray', alpha=1)

    # Berechne den dpi-Wert für die gewünschte Auflösung
    auflösung_breite = 1920
    auflösung_höhe = 1080
    zoll_pro_dpi = 1 / 80  # Standardmäßig etwa 80 dpi pro Zoll
    dpi = max(auflösung_breite / (zoll_pro_dpi * plt.rcParams['figure.figsize'][0]),
              auflösung_höhe / (zoll_pro_dpi * plt.rcParams['figure.figsize'][1]))

    plt.savefig('SAT_TEST_niedersachsen.png',dpi=600)
    #plt.show()


if __name__ == '__main__':
    main()

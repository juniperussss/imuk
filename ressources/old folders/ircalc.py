import rasterio

# Dateipfad zur GeoTIFF-Datei
tiff_file = 'output_image.tiff'

# Öffnen der GeoTIFF-Datei
with rasterio.open(tiff_file) as src:
    # Lies die Bänder der GeoTIFF-Datei (normalerweise gibt es drei Bänder für RGB)
    red_band = src.read(1)
    green_band = src.read(2)
    blue_band = src.read(3)

brightness_threshold = 50  # Passe den Schwellenwert nach Bedarf an
mask = red_band < brightness_threshold
red_band[mask] = 0
green_band[mask] = 0
blue_band[mask] = 0

with rasterio.open('geotiff_datei_bearbeitet.tif', 'w', **src.meta) as dst:
    dst.write(red_band, 1)
    dst.write(green_band, 2)
    dst.write(blue_band, 3)

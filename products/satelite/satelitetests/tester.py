import pyproj

# Definieren Sie die EPSG-Codes für die Projektionen
epsg_code_plate_carree = 4326  # Plate Carrée (Geografische Koordinaten)
epsg_code_lambert_conformal = 9802  # Lambert Conformal mit zentraler Referenz-Längengrad 10

# Erstellen Sie die Proj.4-Projektionsobjekte
lambert_conformal_definition = "+proj=lcc +lat_0=39 +lon_0=10 +lat_1=33 +lat_2=45 +x_0=0 +y_0=0 +datum=WGS84  +no_defs"

lambert_conformal = pyproj.Proj(lambert_conformal_definition)

plate_carree = pyproj.Proj(f"epsg:{epsg_code_plate_carree}")

# Beispielkoordinaten (Längengrad und Breitengrad) in Plate Carrée
lon = 70
lat = 72

# Konvertieren Sie die Koordinaten von Plate Carrée in die Lambert-Conformal-Projektion
x, y = pyproj.transform(plate_carree, lambert_conformal, lon, lat)

# x und y sind jetzt die umgerechneten Koordinaten in der Lambert-Conformal-Projektion
print(x,y)
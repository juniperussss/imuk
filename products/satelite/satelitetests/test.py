from pyproj import Transformer
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857",always_xy=True)
transformer.transform(12, 12)
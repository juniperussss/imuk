import wradlib as wrl
import numpy as np
import warnings
warnings.filterwarnings('ignore')


# We will export this RADOLAN dataset to a GIS compatible format
#wdir = wrl.util.get_wradlib_data_path() #+ '/radolan/grid/'
#filename = 'radolan/misc/raa01-sf_10000-1408102050-dwd---bin.gz'

filename ="DE1200_RV2309181430_000"
#filename = "raa01-rw_10000-latest-dwd---bin"
#filename = wrl.util.get_wradlib_data_file(filename)
#data_raw, meta = wrl.io.read_radolan_composite(filename)

data_raw = wrl.io.open_radolan_dataset(filename).RV
# This is the RADOLAN projection
proj_osr = wrl.georef.create_osr("dwd-radolan")

# Get projected RADOLAN coordinates for corner definition
#xy_raw = wrl.georef.get_radolan_grid(900, 900)
xy_raw = wrl.georef.get_radolan_grid(1200, 1100)

data, xy = wrl.georef.set_raster_origin(data_raw, xy_raw, 'upper')


# create 3 bands
data = np.stack((data, data+100, data+1000))
ds = wrl.georef.create_raster_dataset(data, xy, projection=proj_osr)
wrl.io.write_raster_dataset("geotiff_n.tif", ds, 'GTiff')
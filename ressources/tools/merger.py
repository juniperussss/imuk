import xarray as xr
import numpy as np
import os
import PyNIO as Nio
ds = xr.open_dataset("database/input/icon/2022/9/17/12/t/500/outfile_merged_2022091712_000_004_500_T.grib2", engine="pynio")
db= xr.open_dataset("database/input/icon/2022/9/17/12/fi/500/outfile_merged_2022091712_000_004_500_FI.grib2", engine="pynio")
for v in ds:
    print("{}, {}, {}".format(v, ds[v].attrs["long_name"], ds[v].attrs["units"]))

print(ds.head())

f1=ds.isel( forecast_time0=slice(None, 1))
f2=db.isel( forecast_time0=slice(None, 1))
#df2 = ds.set_index("forecast_time0", drop = False)



#---- open files and read variables

dir_origin = os.getcwd()
dir_Produkt = '../../database/output/500/'
os.chdir(dir_Produkt)





print(f1.variables.keys()) # list of the variables briefly
for i in f1.variables: # main features of the variables
    print(f1.variables[i].long_name, f1.variables[i].name, f1.variables[i].units, f1.variables[i].shape)
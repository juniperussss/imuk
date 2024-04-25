import xarray as xr

ds = xr.open_dataset("/mnt/nvmente/CODE/imuk/database/input/icon/2024/4/23/12/ww/ofile_single-level_2024042312_000_WW.grib2", engine="cfgrib")

lat_han = 52.5
lon_han = 9.75

print(ds["WW"].sel(longitude=lon_han, latitude=lat_han).values.item())
import xarray as xr

ds = xr.open_dataset("/mnt/nvmente/CODE/imuk/database/input/icon/2024/4/23/12/vmax_10m/ofile_2024042312_003_VMAX_10M.grib2", engine="cfgrib")

lat_han = 52.5
lon_han = 9.75

print(ds["fg10"].sel(longitude=lon_han, latitude=lat_han).values.item())
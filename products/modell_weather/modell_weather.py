#Placeholder
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pyproj
import cartopy.feature as cfeature
import os
import Nio, Ngl
import numpy as np
import warnings
from datetime import datetime
import metpy.calc as mpcalc
from metpy.units import units
import ressources.tools.imuktools as imuktools
import argparse
import xarray as xr




###
def picture(vara, varb, number, resx, resy, dir_origin,filenames):
    warnings.filterwarnings("ignore")
    current_date = datetime.utcnow()
    print("EU has started at: ", current_date.strftime('%Y-%m-%d  %H:%M:%S'))
    current_yr = current_date.year
    current_mo = current_date.month
    current_day = current_date.day
    yrmoday = current_date.strftime('%d/%m/%Y')

    # ---- open files and read variables

    dir_shp = os.path.join(dir_origin + '/database/shp/')
    fn_shp = dir_shp + 'DEU/gadm36_DEU_1.shp'
    f0 = Nio.open_file(os.path.join(dir_shp, fn_shp), "r")  # Open shapefile

    lon0 = np.ravel(f0.variables["x"][:])
    lat0 = np.ravel(f0.variables["y"][:])
    segments = f0.variables["segments"]

    dir = os.path.join(dir_origin)  # path of model output
    fn1 = vara  # '/database/input/icon/2022/8/19/00/u/300/outfile_merged_2022081900_000_004_300_U.grib2' #path name of model output
    f1 = Nio.open_file(os.path.join(vara))  # model output definition

    # print(f1.variables.keys()) # list of the variables briefly
    # for i in f1.variables: # main features of the variables
    #   print(f1.variables[i].long_name, f1.variables[i].name, f1.variables[i].units, f1.variables[i].shape)

    ds = xr.load_dataset(os.path.join(vara), engine="cfgrib")
    print(ds)
    lon_start = -10
    lon_end = 28
    lat_start = 60
    lat_end = 35

    fig = plt.figure(figsize=(12.8,7.2))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal(
        central_longitude=10))  # ,central_latitude=52) ) #ccrs.Miller())#
    pyproj.set_use_global_context()
    #ax.coastlines()
    #ax.LAKES()
    ax.add_feature(cfeature.COASTLINE)
    #ax.add_feature(cfeature.LAND)#, facecolor='darkgreen')
    land_110m = cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                    edgecolor='face',
                                    facecolor="darkgreen",#cfeature.COLORS['land'],
                                    zorder=0)
    ax.add_feature(land_110m)


    ocean_110m = cfeature.NaturalEarthFeature('physical', 'ocean', '50m',
                                    edgecolor='face',
                                    facecolor="navy",#cfeature.COLORS['water'],
                                    zorder=0)
    ax.add_feature(ocean_110m)

    ax.set_extent([lon_start, lon_end, lat_start,lat_end], crs=ccrs.PlateCarree())  # Begrenzung auf Europa
    plot = ds.u.plot(
    cmap=plt.cm.coolwarm, transform=ccrs.PlateCarree(), cbar_kwargs={"shrink": 0.6}
    )
    plt.show()




def main():
    ##Parsing Variable Values
    #parser = argparse.ArgumentParser()
    #parser.add_argument('resx')  # 350
    #parser.add_argument('resy')  #
    #parser.add_argument('outputpath')
    #parser.add_argument('inputpath')
    #parser.add_argument('timerangestart')
    #parser.add_argument('timerangestop')
    #parser.add_argument('timerangestepsize')
   # args = parser.parse_args() 
    resx = 945#int(args.resx)
    resy = 480#int(args.resy)
    dir_origin =  "/mnt/nvmente/CODE/imuk" #args.inputpath
    dir_Produkt = "/mnt/nvmente/CODE/imuk/localtest"#args.outputpath
    os.chdir(dir_Produkt)
    ### Cleaning and Setup
    varnumber = 2
    vars = ["u", "v"]
    varlevel = [300, 300]
    start=0
    end=1
    stepsize=3
    #timerange = np.arange(int(args.timerangestart),int(args.timerangestop),int(args.timerangestepsize))
    timerange = np.arange(int(start),int(end),int(stepsize))
    filenames= imuktools.filenames(timerange)
    variablepaths = imuktools.varnames(varnumber, vars,
                                     varlevel,
                                     dir_origin, filenames)
    timestepnumber = 1#len(variablepaths[0])
    for i in range(0,len(timerange)):
        #print(variablepaths[0][i])
        picture(variablepaths[0][i], variablepaths[1][i], i, resx, resy, dir_origin,filenames)
    return


if __name__ == "__main__":
    main()

#plt.show()
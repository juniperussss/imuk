#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 17:31:52 2021

@author: juniperus
"""

import os
from datetime import datetime
from tqdm import tqdm
import numpy as np
import glob
import argparse
#import metview as mv
from cdo import *
import timeout_decorator
import concurrent.futures

#print(cdo.__version__())
cdo = Cdo()
import time
import multiprocessing
from multiprocessing import Pool
import xarray as xr
#import xesmf as xe
import cfgrib
parser = argparse.ArgumentParser()



cdt_date = datetime.utcnow()
print(" has started at: ", cdt_date.strftime('%Y-%m-%d  %H:%M:%S'))
cdt_yr = cdt_date.year
cdt_mo = cdt_date.month
cdt_day = cdt_date.day
cdt_yrmoday = cdt_date.strftime('%Y%m%d')

if int(cdt_date.strftime("%H")) >= 4 and int(cdt_date.strftime("%H")) <= 11:
    init_time_hr = '00'
elif int(cdt_date.strftime("%H")) >= 16 and int(cdt_date.strftime("%H")) <= 23:
    init_time_hr = '12' 
else:
    init_time_hr = '00'#input('Enter the model run time ')
    

#dir_origin= os.getcwd()


parser.add_argument('inputpath')  # 350
parser.add_argument('parentpath')  # 350
args = parser.parse_args()
dir_origin = args.inputpath
dir_parent = args.parentpath#'database/input/icon/'
os.chdir(dir_origin+"/ressources/tools")
print(os.getcwd())
#export PYTHONPATH=$PYTHONPATH:`pwd`
from ressources.tools import imuktools
from ressources.tools.observations import metarrequest

fcst_hrs = imuktools.fcst_hrsf(model='icon')
fcst_hrs_output = []
os.chdir(dir_parent)
for output in fcst_hrs:
    fcst_hrs_string = str(output).zfill(3)
    fcst_hrs_output.append(fcst_hrs_string)

imuktools.cleaning_old_today_folders()
if not os.path.exists('{}/{}/{}/{}'.format(cdt_yr, cdt_mo, cdt_day, init_time_hr)):
    try:
        os.makedirs('{}/{}/{}/{}'.format(cdt_yr, cdt_mo, cdt_day, init_time_hr))
        print('The directory is created successfully')
    except:
        print('Creation of the directory failed')
else: 
    print('The directory already exists')
    
os.path.join( '{}/{}/{}/{}'.format(cdt_yr, cdt_mo, cdt_day, init_time_hr))
os.chdir( '{}/{}/{}/{}'.format(cdt_yr, cdt_mo, cdt_day, init_time_hr))
dir_Nest = os.path.join(os.getcwd())
print('entered into', dir_Nest)

#metarrequest(dir_origin)

import requests
class p(object):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name


global variables

vars=["t","t","t","clct_mod","u","v","relhum","fi","fi","fi","ww","pmsl","tot_prec"]
vars2 = [ "u_10m","v_10m","vmax_10m","t_2m","cape_con","snow_con","u","u","u","u","v","v","v","v", "td_2m"]
levels=['pressure-level','pressure-level','pressure-level','single-level','pressure-level','pressure-level','pressure-level','pressure-level','pressure-level','pressure-level','single-level',
'single-level','single-level']
levels2= ['single-level','single-level','single-level','single-level','single-level' ,'single-level','pressure-level','pressure-level','pressure-level','pressure-level','pressure-level','pressure-level','pressure-level','pressure-level','single-level']

gph=['_500',"_700","_850","","_300","_300","_700","_500","_700","_850","","",""]
gph2= ["","","","","","","_500","_700","_850","_950","_500","_700","_850","_950",""]
#vars=["t","t","t","clct_mod","u","v","relhum","fi","fi","fi","ww","pmsl","tot_prec","u_10m","v_10m","vmax_10m","t_2m","cape_con","snow_con"]
#levels=['pressure-level','pressure-level','pressure-level','single-level','pressure-level','pressure-level','pressure-level','pressure-level','pressure-level','pressure-level','single-level','single-level','single-level','single-level','single-level','single-level','single-level','single-level' ,'single-level']
#gph=['_500',"_700","_850","","_300","_300","_700","_500","_700","_850","","","","","","","","",""]
print(vars+vars2)
variables= list(zip(vars+ vars2,levels + levels2, gph+gph2))
variables2 =list(zip(vars2,levels2, gph2))
number=np.arange(0,len(variables))
number2=np.arange(0,len(variables2))


#print(variables[0][0])
#same variable issue for temperature and geopotential height !
#print(variables["t"][1])
url_base = 'https://opendata.dwd.de/weather/nwp/icon/grib/'




grids= dir_origin +'/database/ICON_GLOBAL2EUAU_025_EASY/target_grid_EUAU_025.txt'
weights= dir_origin +'/database/ICON_GLOBAL2EUAU_025_EASY/weights_icogl2world_025_EUAU.nc'

#try:
 #   cdo = Cdo()
#except:

#cdo=Cdo("/home/alex/miniforge3/envs/imuk/bin/cdo")
#cdo=Cdo()
cdo.debug = False
def varrequest(number):
    #try: 
        print(f'/_{variables[number][1]}'+variables[number][2][1:])
        var= variables[number][0]

        os.makedirs(dir_Nest + f'/{var}'+f'/{variables[number][2][1:]}')
        os.path.join(dir_Nest + f'/{var}'+f'/{variables[number][2][1:]}')
        os.chdir(dir_Nest + f'/{var}'+f'/{variables[number][2][1:]}')

        for hour in fcst_hrs:
            if hour == 0 and var == "vmax_10m":  # vmax_10m is not available for 0 hour
                continue
            url_data = url_base +'{}/{}/icon_global_icosahedral_{}_{}{}_{}{}_{}.grib2.bz2'.format(
                init_time_hr, var, variables[number][1], cdt_yrmoday, init_time_hr, str(hour).zfill(3), variables[number][2], str(var).upper())
            #print(url_data)
            data_request = requests.get(url_data, stream=True)
            if data_request.status_code == 200:
                print(url_data)
                print('{}'.format(var), u'\u2714')

            with open('icon_global_icosahedral_{}_{}{}_{}{}_{}.grib2.bz2'.format(
                    variables[number][1], cdt_yrmoday, init_time_hr, str(hour).zfill(3), variables[number][2], str(var).upper()), 'wb') as f:
                f.write(data_request.content)

            zip_command = 'bzip2 -d *.bz2'
            os.system(zip_command)

            ifile = dir_Nest + '/{}/{}/icon_global_icosahedral_{}_{}{}_{}{}_{}.grib2'.format(
                var, variables[number][2][1:], variables[number][1], cdt_yrmoday, init_time_hr, str(hour).zfill(3), variables[number][2], str(var).upper())
            print(ifile)

            # cdo.sellonlatbox('-75,75,5,80', input=ifile, output='haha.grib2') #not necessary for this step
            #@timeout_decorator.timeout(300) # 300 Sekunden = 5 Minuten
            def remap(ifile, grids, weights):
                print("begin remapping of ", ifile)
                cdo.remap(grids, weights, input=ifile, output='ofile_{}_{}_{}_{}'.format(
                    ifile.split('_')[-4:][0], ifile.split('_')[-4:][1],
                    ifile.split('_')[-4:][2], ifile.split('_')[-4:][3]),
                    options='-f grb2')
                return
                
            def remap_xarray(ifile, grids, weights):
                # Laden des Eingabedatensatzes
                ds = xr.open_dataset(ifile)
                print(ds)
                output_file_name ='ofile_{}_{}_{}_{}'.format(
                    ifile.split('_')[-4:][0], ifile.split('_')[-4:][1],
                    ifile.split('_')[-4:][2], ifile.split('_')[-4:][3])
                # Laden des Gitter- und Gewichtsdatensatzes
                with open(grids, 'r') as f:
                    lines = f.readlines()
                    xfirst = float(lines[3].split('=')[1].strip())
                    xinc = float(lines[5].split('=')[1].strip())
                    yfirst = float(lines[6].split('=')[1].strip())
                    yinc = float(lines[7].split('=')[1].strip())
                    xsize = int(lines[2].split('=')[1].strip())
                    ysize = int(lines[3].split('=')[1].strip())
                
                # Erstellen des Zielgitters
                ds_out = xr.Dataset({'lon': (['lon'], np.arange(xfirst, xfirst + xinc * xsize, xinc)),
                                  'lat': (['lat'], np.arange(yfirst, yfirst + yinc * ysize, yinc))})
                
                regridder = xe.Regridder(ds, ds_out, 'bilinear', filename=weights)
                
                # Anwenden des Remappings
                ds_remapped = regridder(ds)
                
                # Speichern des remappten Datensatzes im GRIB-Format
                ds_remapped.to_netcdf(output_file_name +".nc", format='NETCDF3_CLASSIC')
                
                # Konvertieren der NetCDF-Datei in GRIB
                with cfgrib.open_dataset(output_file_name +".nc", 'r') as ds_grib:
                    ds_grib.to_grib(output_file_name +".grib2")
                return
            
            #def remap_metview(ifile, grids, weights):
                #ds = xr.open_dataset(ifile,engine="cfgrib")
             #   t = mv.read(ifile)

              #  output_file_name ='ofile_{}_{}_{}_{}'.format(
                #    ifile.split('_')[-4:][0], ifile.split('_')[-4:][1],
               #     ifile.split('_')[-4:][2], ifile.split('_')[-4:][3])
                # Laden des Gitter- und Gewichtsdatensatzes
                #with open(grids, 'r') as f:
                 #   lines = f.readlines()
                  #  xfirst = float(lines[3].split('=')[1].strip())
                   # xinc = float(lines[5].split('=')[1].strip())
                    #yfirst = float(lines[6].split('=')[1].strip())
                   # yinc = float(lines[7].split('=')[1].strip())
                  #  xsize = int(lines[2].split('=')[1].strip())
                 #   ysize = int(lines[3].split('=')[1].strip())

                #f2 = mv.read(data=t,
                 #           grid=[xinc,yinc],
                  #          area=[yfirst,xfirst,yfirst+ysize*yinc,xfirst+xsize*xinc]) # S,W,N,E
                #return

            #remap_xarray(ifile,grids,weights)
            remap(ifile,grids,weights)
            #try:
             ##   remap_with_timeout(ifile, grids, weights)
            #except timeout_decorator.TimeoutError:
               # print("Zeitüberschreitung: Der Vorgang wurde nach 5 Minuten abgebrochen.")

            #pbar.update()


        for ifile in glob.glob('*icosahedral*', recursive=True):
            print("Removing ", ifile)
            os.remove(ifile)


        os.chdir(dir_origin)
        #print(os.path.abspath(os.getcwd()) +" has completed at: ", cdt_date.strftime('%Y-%m-%d  %H:%M:%S'))
    #except Exception as err:
     #   print(err)

        return

#imuktools.archiving()

def start_pool(cores=4):
    # Anzahl der verfügbaren CPU-Kerne abrufen
    num_cores = multiprocessing.cpu_count()
    
    # Entweder 3 Kerne oder alle Kerne - 1 verwenden, je nachdem, was kleiner ist
    num_processes = min(cores, num_cores - 1)

    # Pool mit der entsprechenden Anzahl von Prozessen erstellen
    pool = multiprocessing.Pool(processes=num_processes)
    
    return pool

if __name__ == "__main__":
    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(varrequest, number, timeout=300)
    
    #print("start secound vars")
    #with concurrent.futures.ProcessPoolExecutor() as executor2:
     #   executor2.map(varrequest, number2)

    #with  start_pool(cores=10) as pool:
     #   pool.map(varrequest, number)
      #  print("start secound vars")
       # pool.map(varrequest, number2)

    #varrequest(0)
    imuktools.cleaning_old_folders()
    print("--- %s seconds ---" % (time.time() - start_time))

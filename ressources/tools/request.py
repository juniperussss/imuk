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
#import timeout_decorator
import concurrent.futures
from multiprocess import Pool
import multiprocess

#print(cdo.__version__())
cdo = Cdo()
import time
import multiprocessing
#from multiprocessing import Pool
import xarray as xr
#import xesmf as xe
#import cfgrib

import signal

parser = argparse.ArgumentParser()


def timeout_handler(signum, frame):
   raise TimeoutError("Das Skript hat die maximale Laufzeit überschritten und wurde abgebrochen.")



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

metarrequest(dir_origin)

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





cdo.debug = False

def fetch_data(url, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            data_request = requests.get(url, stream=True)
            if data_request.status_code == 200:
                return data_request
            else:
                print(f"Attempt {attempt + 1} failed with status code {data_request.status_code}")
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
        
        if attempt < max_retries - 1:
            print("Retrying download...")
            time.sleep(delay)
    
    print("All attempts failed")
    return None

def varrequest(number):
        var= variables[number][0]

        os.makedirs(dir_Nest + f'/{var}'+f'/{variables[number][2][1:]}')
        os.path.join(dir_Nest + f'/{var}'+f'/{variables[number][2][1:]}')
        os.chdir(dir_Nest + f'/{var}'+f'/{variables[number][2][1:]}')

        for hour in fcst_hrs:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(180)  # Timeout in Sekunden
            try:
                if hour == 0 and var == "vmax_10m":  # vmax_10m is not available for 0 hour
                    continue
                url_data = url_base +'{}/{}/icon_global_icosahedral_{}_{}{}_{}{}_{}.grib2.bz2'.format(
                    init_time_hr, var, variables[number][1], cdt_yrmoday, init_time_hr, str(hour).zfill(3), variables[number][2], str(var).upper())

                data_request = fetch_data(url_data)
                if data_request:
                   #print("Download succeeded")
                   pass
                else:
                    print("Download failed")

                with open('icon_global_icosahedral_{}_{}{}_{}{}_{}.grib2.bz2'.format(
                        variables[number][1], cdt_yrmoday, init_time_hr, str(hour).zfill(3), variables[number][2], str(var).upper()), 'wb') as f:
                    f.write(data_request.content)

                zip_command = 'bzip2 -d *.bz2'
            
                os.system(zip_command)


                grids= dir_origin +'/database/ICON_GLOBAL2EUAU_025_EASY/target_grid_EUAU_025.txt'
                weights= dir_origin +'/database/ICON_GLOBAL2EUAU_025_EASY/weights_icogl2world_025_EUAU.nc'
                ifile = dir_Nest + '/{}/{}/icon_global_icosahedral_{}_{}{}_{}{}_{}.grib2'.format(
                    var, variables[number][2][1:], variables[number][1], cdt_yrmoday, init_time_hr, str(hour).zfill(3), variables[number][2], str(var).upper())
                
                def remap(ifile, grids, weights):
                    #print("begin remapping of ", ifile)
                    cdo.remap(grids, weights, input=ifile, output='ofile_{}_{}_{}_{}'.format(
                        ifile.split('_')[-4:][0], ifile.split('_')[-4:][1],
                        ifile.split('_')[-4:][2], ifile.split('_')[-4:][3]),
                        options='-f grb2')
                    return
                remap(ifile,grids,weights)
            
            except Exception as err:
                print(err)
                print("Probleme bei", var, variables[number][1],variables[number][2])
            finally:
            # Deaktiviere den Alarm, falls das Skript vorher beendet wird
                signal.alarm(0)

        os.chdir(dir_origin)
        print( var, variables[number][1],variables[number][2], "fertig")
 


        return



if __name__ == "__main__":
    start_time = time.time()
   # number,variables,url_base,dir_Nest,cdt_yrmoday,dir_origin,fcst_hrs,init_time_hr =basics()

   # pool = Pool()
    #with Pool() as pool:
    #pool.map(varrequest, number)
    #pool.close()
    #pool.join()
    with Pool() as pool:
            pool.map(varrequest, number)
            pool.close()
            pool.join()
 
    imuktools.cleaning_old_folders()
    print("--- %s seconds ---" % (time.time() - start_time))

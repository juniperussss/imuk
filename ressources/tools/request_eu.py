#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 17:31:52 2021

@author: juniperus
"""

import os
from datetime import datetime
# from tqdm import tqdm
import numpy as np
import glob
import argparse

import time
#from multiprocessing import set_start_method

import imuktools
#from multiprocessing import Pool
#from multiprocessing import get_context
from multiprocess import Pool
#import requests

import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Das Skript hat die maximale Laufzeit überschritten und wurde abgebrochen.")


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
    init_time_hr = '00'  # input('Enter the model run time ')

# dir_origin= os.getcwd()


parser.add_argument('inputpath')  # 350
parser.add_argument('parentpath')  # 350
args = parser.parse_args()
dir_origin = args.inputpath
dir_parent = args.parentpath  # 'database/input/icon-eu/'
if not os.path.exists(dir_parent):
    os.makedirs(dir_parent)
os.chdir(dir_origin + "/ressources/tools")
print(os.getcwd())
# export PYTHONPATH=$PYTHONPATH:`pwd`
from ressources.tools import imuktools

# from ressources.tools.observations import metarrequest

fcst_hrs = imuktools.fcst_hrsf(model='icon-eu')
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

os.path.join('{}/{}/{}/{}'.format(cdt_yr, cdt_mo, cdt_day, init_time_hr))
os.chdir('{}/{}/{}/{}'.format(cdt_yr, cdt_mo, cdt_day, init_time_hr))
dir_Nest = os.path.join(os.getcwd())
print('entered into', dir_Nest)
# metarrequest(dir_origin)
import requests


class p(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


global variables

vars = ["t", "t", "t", "clct_mod", "u", "v", "relhum", "fi", "fi", "fi", "ww", "pmsl", "tot_prec", "u_10m", "v_10m",
        "vmax_10m", "t_2m", "cape_con", "snow_con","u","u","u","u","v","v","v","v", "td_2m"]
levels = ['pressure-level', 'pressure-level', 'pressure-level', 'single-level', 'pressure-level', 'pressure-level',
        'pressure-level', 'pressure-level', 'pressure-level', 'pressure-level', 'single-level', 'single-level',
        'single-level', 'single-level', 'single-level', 'single-level', 'single-level', 'single-level',
        'single-level','pressure-level','pressure-level','pressure-level','pressure-level','pressure-level','pressure-level','pressure-level','pressure-level','single-level']
gph = ['_500', "_700", "_850", "", "_300", "_300", "_700", "_500", "_700", "_850", "", "", "", "", "", "", "", "", "","_500","_700","_850","_950","_500","_700","_850","_950",""]
variables = list(zip(vars, levels, gph))
number=np.arange(0,len(variables))


# print(variables[0][0])
# same variable issue for temperature and geopotential height !
# print(variables["t"][1])
url_base = 'https://opendata.dwd.de/weather/nwp/icon-eu/grib/'
def varrequest(number):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(60)  # Timeout in Sekunden
    try:
        #print(f'/_{variables[number][1]}'+variables[number][2][1:])
        var = variables[number][0]
        #print(var)


        os.makedirs(dir_Nest + f'/{var}' + f'/{variables[number][2][1:]}')
        os.path.join(dir_Nest + f'/{var}' + f'/{variables[number][2][1:]}')
        os.chdir(dir_Nest + f'/{var}' + f'/{variables[number][2][1:]}')

        for hour in fcst_hrs:
            url_data = url_base + '{}/{}/icon-eu_europe_regular-lat-lon_{}_{}{}_{}{}_{}.grib2.bz2'.format(
                init_time_hr, var, variables[number][1], cdt_yrmoday, init_time_hr, str(hour).zfill(3),
                variables[number][2], str(var).upper())
            # print(url_data)
            data_request = requests.get(url_data, stream=True)
            #if data_request.status_code == 200:
                #print(url_data)
                #print('{}'.format(var), u'\u2714')

            with open('icon-eu_europe_regular-lat-lon_{}_{}{}_{}{}_{}.grib2.bz2'.format(
                    variables[number][1], cdt_yrmoday, init_time_hr, str(hour).zfill(3), variables[number][2],
                    str(var).upper()), 'wb') as f:
                f.write(data_request.content)

            zip_command = 'bzip2 -d *.bz2'
            os.system(zip_command)
            print(var,variables[number][2],hour)
        os.chdir(dir_origin)
       # print(os.path.abspath(os.getcwd()) + " has completed at: ", cdt_date.strftime('%Y-%m-%d  %H:%M:%S'))

    except Exception as err:
        print(err)

    finally:
    # Deaktiviere den Alarm, falls das Skript vorher beendet wird
        signal.alarm(0)
        

    return

# imuktools.archiving()
#



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

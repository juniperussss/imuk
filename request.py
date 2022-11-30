#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 17:31:52 2021

@author: juniperus
"""

import os, sys
from datetime import datetime, timedelta
#from tqdm import tqdm
import numpy as np
import glob
import argparse
import cleaner

parser = argparse.ArgumentParser()

fcst_hrs = cleaner.fcst_hrsf()
fcst_hrs_output = []
for output in fcst_hrs:
    fcst_hrs_string = str(output).zfill(3)
    fcst_hrs_output.append(fcst_hrs_string)


print(fcst_hrs)
cdt_date = datetime.utcnow()
print(" has started at: ", cdt_date.strftime('%Y-%m-%d  %H:%M:%S'))
cdt_yr = cdt_date.year
cdt_mo = cdt_date.month
cdt_day = cdt_date.day
cdt_yrmoday = cdt_date.strftime('%Y%m%d')

if int(cdt_date.strftime("%H")) >= 3 and int(cdt_date.strftime("%H")) <= 11:
    init_time_hr = '00'
elif int(cdt_date.strftime("%H")) >= 15 and int(cdt_date.strftime("%H")) <= 23:
    init_time_hr = '12' 
else:
    init_time_hr = '00'#input('Enter the model run time ')
    

#dir_origin= os.getcwd()


parser.add_argument('inputpath')  # 350
parser.add_argument('parentpath')  # 350
args = parser.parse_args()
dir_origin = args.inputpath
dir_parent = args.parentpath#'database/input/icon/'
os.chdir(dir_parent)
cleaner.cleaning_old_today_folders()
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

import requests
class p(object):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

# variables = {"t": ['pressure-level', '_500'],
#             "u": ['pressure-level', '_300'], 
#             "v": ['pressure-level', '_300'],
#             "relhum": ['pressure-level', '_700'],
#               "fi": ['pressure-level', '_700']}

variables = {p('t'): ['pressure-level', '_500'],
             p('t'): ['pressure-level', '_700'],
             p('t'): ['pressure-level', '_850'],
             p('clct_mod'): ['single-level', ''],
             p('u'): ['pressure-level', '_300'],
             p('v'): ['pressure-level', '_300'],
             p('relhum'): ['pressure-level', '_700'],
             p('fi'): ['pressure-level', '_500'],
             p('fi'): ['pressure-level', '_700'],
             p('fi'): ['pressure-level', '_850'],
             p("ww"): ['single-level', ''],
             p("pmsl"): ['single-level', ''],
             p("tot_prec"): ['single-level', '']}
#same variable issue for temperature and geopotential height !

url_base = 'https://opendata.dwd.de/weather/nwp/icon/grib/'

from cdo import Cdo

cdo = Cdo()
cdo.debug = True

grids= dir_origin +'/database/ICON_GLOBAL2EUAU_025_EASY/target_grid_EUAU_025.txt'
weights= dir_origin +'/database/ICON_GLOBAL2EUAU_025_EASY/weights_icogl2world_025_EUAU.nc'

#with tqdm(total=len(variables), position=0, leave=True, colour='green') as pbar:
for var in variables:
    os.makedirs(dir_Nest + f'/{var}'+f'/{variables[var][1][1:]}')
    os.path.join(dir_Nest + f'/{var}'+f'/{variables[var][1][1:]}')
    os.chdir(dir_Nest + f'/{var}'+f'/{variables[var][1][1:]}')

    for hour in fcst_hrs:

        url_data = url_base +'{}/{}/icon_global_icosahedral_{}_{}{}_{}{}_{}.grib2.bz2'.format(
            init_time_hr, var, variables[var][0], cdt_yrmoday, init_time_hr, str(hour).zfill(3), variables[var][1], str(var).upper())

        data_request = requests.get(url_data, stream=True)
        if data_request.status_code == 200:
            print(url_data)
            print('{}'.format(var), u'\u2714')

        with open('icon_global_icosahedral_{}_{}{}_{}{}_{}.grib2.bz2'.format(
                variables[var][0], cdt_yrmoday, init_time_hr, str(hour).zfill(3), variables[var][1], str(var).upper()), 'wb') as f:
            f.write(data_request.content)

        zip_command = 'bzip2 -d *.bz2'
        os.system(zip_command)

        ifile = dir_Nest + '/{}/{}/icon_global_icosahedral_{}_{}{}_{}{}_{}.grib2'.format(
            var, variables[var][1][1:], variables[var][0], cdt_yrmoday, init_time_hr, str(hour).zfill(3), variables[var][1], str(var).upper())
        # print(ifile)

        # cdo.sellonlatbox('-75,75,5,80', input=ifile, output='haha.grib2') #not necessary for this step
        cdo.remap(grids, weights, input=ifile, output='ofile_{}_{}_{}_{}'.format(
            ifile.split('_')[-4:][0], ifile.split('_')[-4:][1],
            ifile.split('_')[-4:][2], ifile.split('_')[-4:][3]),
            options='-f grb2')

        #pbar.update()


    # cdo.mergetime(input='*ofile*', output='outfile_merged_{}{}_{}_{}{}_{}.grib2'.format(
        # cdt_yrmoday, init_time_hr,
        # str(fcst_hrs[0]).zfill(3), str(fcst_hrs[-1]).zfill(3),
        # variables[var][1], str(var).upper(), options='-f grb2'))

    for ifile in glob.glob('*icosahedral*', recursive=True):
        print("Removing ", ifile)
        os.remove(ifile)

    # for ofile in glob.glob('*ofile*', recursive=True):
        # print("Removing ", ofile)
        # os.remove(ofile)

    os.chdir(dir_origin)
    print(os.path.abspath(os.getcwd()) +" has completed at: ", cdt_date.strftime('%Y-%m-%d  %H:%M:%S'))


#cleaner.cleaning_old_folders()
#cleaner.archiving()

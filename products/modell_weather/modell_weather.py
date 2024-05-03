#!/usr/bin/env python3
# -*- coding: utf-8 -*-
    
#---- calling for the necessary libraries
import os
import Nio, Ngl
import numpy as np
import warnings
from datetime import datetime
import metpy.calc as mpcalc
import argparse
import pandas as pd
import numpy.ma as ma
#from icecream import ic
from multiprocessing import Pool
import time
import ressources.tools.imuktools as imuktools
import geopandas as gpd
from sklearn.cluster import KMeans, DBSCAN
from shapely.geometry import Point
import xarray as xr
###
#def picture(vara,varb,varc,vard,number,resx,resy,dir_origin,filenames,rain_parameter):
def picture(vara,varb,varc,vard,number,resx,resy,dir_origin,filenames,rain_parameter,model):
    warnings.filterwarnings("ignore")
    current_date = datetime.utcnow()
    print("EU has started at: ", current_date.strftime('%Y-%m-%d  %H:%M:%S'))
    current_yr = current_date.year
    current_mo = current_date.month
    current_day = current_date.day
    yrmoday = current_date.strftime('%d/%m/%Y')

    #---- open files and read variables

    dir_shp     = os.path.join( dir_origin+'/database/shp/')
    fn_shp      = dir_shp + 'DEU/gadm36_DEU_1.shp'
    f0 = Nio.open_file(os.path.join(dir_shp, fn_shp), "r")   # Open shapefile

    lon0     = np.ravel(f0.variables["x"][:])
    lat0      = np.ravel(f0.variables["y"][:])
    segments = f0.variables["segments"]

    dir         = os.path.join(dir_origin) #path of model output
    fn1          = vara#dir + '/database/input/icon/2022/8/2/00/clct_mod/outfile_merged_2022080200_000_004_CLCT_MOD.grib2' #path name of model output
    f1           = Nio.open_file(os.path.join(vara))#dir, fn1)) #model output definition


    lon1 = ma.round(f1.variables['lon_0'][:] - 360,2)
    lat1 = ma.round(f1.variables['lat_0'][:],2)
    clct = ma.round(f1.variables['VAR_0_6_199_P0_L1_GLL0'][:,:],2)

    dir         = os.path.join(dir_origin) #path of model output
    fn2          = varb #dir + '/database/input/icon/2022/8/2/00/pmsl/outfile_merged_2022080200_000_004_PMSL.grib2' #path name of model output
    f2           = Nio.open_file(os.path.join(varb))#dir, fn2)) #model output definition


    lon2 = ma.round(f2.variables['lon_0'][:] - 360,2)
    lat2 = ma.round(f2.variables['lat_0'][:],2)
    pmsl = ma.round(f2.variables['PRMSL_P0_L101_GLL0'][:,:]/100,2)


    dir         = os.path.join(dir_origin) #path of model output
    fn3          = varc# dir + '/database/input/icon/2022/8/2/00/tot_prec/outfile_merged_2022080200_000_004_TOT_PREC.grib2' #path name of model output
    f3          = Nio.open_file(os.path.join(varc))#dir, fn3)) #model output definition

    
    lon3 = ma.round(f3.variables['lon_0'][:] - 360,2)
    lat3 = ma.round(f3.variables['lat_0'][:],2)
    #rain = f3.variables['TPRATE_P8_L1_GLL0_acc'][:,:]
    rain = ma.round(np.array(f3.variables['TPRATE_P8_L1_GLL0_acc'][:,:]),2)
    if number != 0:
        dir         = os.path.join(dir_origin) #path of model output
        fn3p          = rain_parameter# dir + '/database/input/icon/2022/8/2/00/tot_prec/outfile_merged_2022080200_000_004_TOT_PREC.grib2' #path name of model output
        f3p          = Nio.open_file(os.path.join(rain_parameter))#dir, fn3)) #model output definition
        rain_previous = ma.round(np.array(f3p.variables['TPRATE_P8_L1_GLL0_acc'][:,:]),2)
        rain_instant = rain - rain_previous
    else:
      rain_instant = rain 

    dir         = os.path.join(dir_origin) #path of model output
    fn4         = vard# dir + '/database/input/icon/2022/8/2/00/tot_prec/outfile_merged_2022080200_000_004_TOT_PREC.grib2' #path name of model output
    f4          = Nio.open_file(os.path.join(vard))#dir, fn3)) #model output definition

    
    lon4 = ma.round(f4.variables['lon_0'][:] - 360,2)
    lat4= ma.round(f4.variables['lat_0'][:],2)
    #print(f4.variables)
    ww = f4.variables['WIWW_P0_L1_GLL0'][:,:]

    print(dir_origin)
    data = pd.read_csv(dir_origin+'/ressources/Data/metar_groundlevel.csv')

    def cluster (data):
        df=data
        def get_weather_priority(weather_symbol,station):
            #print("alla",weather_symbol)
            thunderletters = ["{","|","2","#","%","&"]
            stationlist = ["EDDV"]

            if weather_symbol in thunderletters :
                priority = 4
            elif weather_symbol is None:
                priority = 0
            elif station in stationlist:
                priority = 10
            else:
                priority = 1


            return priority

        num_clusters = 80
        #df['priority'] = df.apply(lambda row: get_weather_priority(row['weathersymbol'], row['station']), axis=1)
        dff = df[df['weathersymbol'].notnull() & (df['weathersymbol'] != '')]

        dff['priority'] = dff.apply(lambda row: get_weather_priority(row['weathersymbol'], row['station']), axis=1)

        dffs = dff[['lat', 'lon', 'priority']]
        #data = df[['lat', 'lon', 'priority']]


        #kmeans = KMeans(n_clusters=num_clusters)
       # dbscan = DBSCAN(eps=0.5, min_samples=15)

        # Die Cluster-Labels berechnen
        kmeans = KMeans(n_clusters=num_clusters)
        dff['cluster_label'] = kmeans.fit_predict(dffs)
        data = dff.groupby('cluster_label').apply(lambda group: group.loc[group['priority'].idxmax()])
        return data

    data = cluster(data)


    lon5= data['lon'].tolist()
    lat5= data['lat'].tolist()
    wwsym= data['weathersymbol'].tolist()
    wwcolour= data['weathercolour'].tolist()

    #---- Preliminaries (2)

    #clct = mpcalc.smooth_n_point(clct, 9, 4)
    pmsl = mpcalc.smooth_n_point(pmsl, 9, 4)
    #rain = mpcalc.smooth_n_point(rain, 9, 4)



    #---- Initial Time

    variable_name = [var for var in f1.variables.keys() if "VAR_0_6_199_P0_L1_GLL0" in var][0]
    init_time = f1.variables[variable_name].attributes['initial_time']
    init_time = init_time.split('/')
    init_time[2] = init_time[2].split('(')
    init_time_hr = init_time[2][1][:-4]
    init_time_day = init_time[1]
    init_time_mo = init_time[0]
    init_time_yr = init_time[2][0]
    initial_date = datetime(int(init_time_yr), int(init_time_mo), int(init_time_day), int(init_time_hr))
    initial_time = initial_date.strftime('%d/%m/%Y %H') +'Z'


    wkres           =  Ngl.Resources()                  #-- generate an resources object for workstation
    wkres.wkBackgroundColor = 'white'
    wkres.wkForegroundColor = 'white'
    wkres.wkWidth   = 3*resx # 3840                             #-- width of workstation
    wkres.wkHeight  = 3*resx #3840#2560                             #-- height of workstation
    wks_type        = "png"    #-- output type of workstation
    wks = Ngl.open_wks(wks_type, 'modell_weather_'+model+"_" + filenames[number], wkres)#-- open workstation

    #---- Resources

    #---- Shapefile Resources

    plres                  = Ngl.Resources()       # resources for polylines
    plres.gsLineColor      = "black"
    plres.gsLineThicknessF = 0                # default is 1.0
    plres.gsSegments       = segments[:,0] #province borders


    #---- Basemap Resources

    mpres = Ngl.Resources()
    mpres.nglMaximize       = True #expanding the draw
    mpres.nglDraw           = False #-- don't draw plot
    mpres.nglFrame          = False #-- don't advance frame


    mpres.mpPerimOn    = True
    mpres.mpPerimLineThicknessF = 4.

    mpres.mpOutlineOn                   = True #-- turn on map outlines
    mpres.mpGeophysicalLineColor        = "black" #boundary color
    mpres.mpGeophysicalLineThicknessF   = (resx / 1920) * 2.0   # -- line thickness of coastal bo1 minutrders
    mpres.mpDataBaseVersion             = "MediumRes"  #Map resolution
    mpres.mpDataResolution              = 'Finest' #Data resolution
    mpres.mpDataSetName                 = "Earth..4"  # -- set map data base version

    mpres.mpLimitMode = "LatLon" #-- limiting the map via lat/lon
    mpres.mpMinLatF = 37  # min(lat1) #-- min latitude
    mpres.mpMaxLatF = 60  # max(lat1) #-- max latitude
    mpres.mpMinLonF = -8 # min(lon1) #-- min longitude
    mpres.mpMaxLonF = 25  # max(lon1) #-- max longtitude

    # Converting the Lambert Perspective Options
    mpres.mpProjection         = "LambertConformal" #projection type
    mpres.mpLambertMeridianF   = 10 #(mpres.mpMinLonF + mpres.mpMaxLonF) / 2 #reference longitude
    diff_lon = (mpres.mpMaxLonF-mpres.mpMinLonF)
    diff_lat = (mpres.mpMaxLatF-mpres.mpMinLatF)
    domain_area = diff_lon*diff_lat



    mpres.mpFillOn               = True  # -- turn on fill for map areas.
    mpres.mpLandFillColor        = "darkgreen"  # -- fill color land -darkslategray
    mpres.mpOceanFillColor       = 'navy' # -- fill color ocean -black
    mpres.mpInlandWaterFillColor = 'navy'  # -- fill color inland water
    mpres.mpAreaMaskingOn        = True


    mpres.mpOutlineBoundarySets  = "national"  # -- "or geophysical"
    mpres.mpOutlineSpecifiers    = "conterminous us: states"  # -- plot state boundaries
    mpres.mpNationalLineThicknessF = 0
    mpres.mpNationalLineColor      = 'black'
    mpres.mpGridAndLimbOn = True
    mpres.mpGridLineColor = 'black'
    mpres.mpGridLatSpacingF     = 10.  # -- grid spacing for latitude
    mpres.mpGridLonSpacingF     = 20.  # -- grid spacing for longitude
    mpres.mpGridLineDashPattern = 3  # -- dash pattern for grid lines

    mpres.tmXBLabelsOn = False
    mpres.tmXTLabelsOn = False
    mpres.tmYRLabelsOn = False
    mpres.tmYLLabelsOn = False
    mpres.tmXBBorderOn = False
    mpres.tmXTBorderOn = False
    mpres.tmYRBorderOn = False
    mpres.tmYLBorderOn = False
    mpres.tmXBOn       = False
    mpres.tmXTOn       = False
    mpres.tmYROn       = False
    mpres.tmYLOn       = False

    #---- Variable (1) Resources

    var1res                 =  Ngl.Resources()
    var1res.nglDraw         =  False #-- don't draw plot
    var1res.nglFrame        =  False

    var1res.cnFillOn        =  True
    var1res.cnFillMode      = 'AreaFill' #cell filling typ5
    var1res.cnLineLabelsOn = False
    # var1res.cnFillMode = not necessary
    # var1res.cnLevelFlags = 'LineAndLabel'
    var1res.cnLinesOn = False


    var1res.pmLabelBarDisplayMode = 'Never'


    cmap_colors = Ngl.read_colormap_file("MPL_gist_gray")
    cmap_colors = np.insert(cmap_colors, 0, [0,0,0,0], axis=0)


    var1res.cnFillPalette    = cmap_colors #-- set the0 colormap to be used or 'NCL_default'

    var1res.cnLevelSelectionMode = "ManualLevels"
    # var1res.cnLevels             = [0.001, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]
    var1res.cnMinLevelValF       = 0.01
    var1res.cnMaxLevelValF       = 1.01
    var1res.cnLevelSpacingF      = 0.1
    var1res.cnFillOpacityF       = 0.85
    var1res.cnNoDataLabelString  = 'No Variable Data'
    var1res.cnConstFLabelString  = 'No Variable Data'

    var1res.lbOrientation            = "horizontal" #-- horizontal labelbar
    var1res.lbTitleString            = '~F34~0~F~C' #f1.variables[list(f1.variables.items())[0][0]].units
    var1res.pmLabelBarOrthogonalPosF = -0.05
    # var1res.pmLabelBarParallelPosF   = 0.25 #-- move labelbar upward
    var1res.lbLabelFontHeightF       = 0.008 #-- labelbar labe font size
    var1res.lbBoxMinorExtentF        = 0.12 #-- decrease height of
    # var1res.lbBoxLinesOn             = True
    var1res.lbTitleFontHeightF       = 0.008 #label title font height
    var1res.lbTitleOffsetF           = -0.40 #title distance from the label
    var1res.lbBoxEndCapStyle         = "TriangleBothEnds"


    var1res.sfXArray = lon1 # processing of longitudes arrays
    var1res.sfYArray = lat1 # processing of latitudes arrays

     #---- Variable (2) Resources

    var2res                 =  Ngl.Resources()
    var2res.nglDraw         =  False #-- don't draw plot
    var2res.nglFrame        =  False

    var2res.cnFillOn = False
    # var2res.cnFillMode = not necessary
    var2res.cnLevelFlags = 'LineAndLabel'
    var2res.cnLinesOn = True
    var2res.cnLineThicknessF = 11.5
    var2res.cnLineColor = 'black'
    #var2res.cnLineLabelBackgroundColor = -1
    var2res.cnLineLabelFontColor = 'black'
    var2res.cnLineLabelsOn = True
    var2res.cnLineLabelPlacementMode = "computed" #randomized places labels wrong, constant doesnt draw high/lows
    var2res.cnLabelMasking = True #mimic behavior of constant line label placement mode
    var2res.cnLineLabelBackgroundColor="transparent"
    var2res.cnLineLabelInterval  = 1 #Label on every line
    var2res.cnConstFLabelConstantSpacingF = 1
    var2res.cnInfoLabelOn = False
    var2res.cnLineLabelFont = "times-bold"
    var2res.cnLineLabelFontHeightF = 0.008
    var2res.pmLabelBarDisplayMode = 'Never'

    var2res.cnLevelSelectionMode = "ManualLevels"
    # var2res.cnLevels             = [0.001, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]
    var2res.cnMinLevelValF       =  950
    var2res.cnMaxLevelValF       = 1100
    var2res.cnLevelSpacingF      = 5
    # var2res.cnConpackParams = [ "HLX:20, HLY:20" ]

    # var2res.cnFillOpacityF = 0.85
    var2res.cnLowLabelsOn = True
    var2res.cnHighLabelsOn = True
    var2res.cnHighLabelString = "H"
    var2res.cnLowLabelString = "T"
    var2res.cnHighLabelFontColor = 'white'
    var2res.cnLowLabelFontColor = 'white'
    #ar2res.cnHighLowLabelOverlapMode =
    # var2res.cnLowLabelFontHeightF = 0.012 #larger L labels
    # var2res.cnHighLabelFontHeightF = 0.020 #larger H labels
    var2res.cnLowLabelBackgroundColor = "Transparent"
    var2res.cnHighLabelBackgroundColor = -1

    var2res.sfXArray = lon2 # processing of longitudes arrays
    var2res.sfYArray = lat2 # processing of latitudes arrays

    #---- Variable (3) Resources
    var3res                 =  Ngl.Resources()
    var3res.nglDraw         =  False #-- don't draw plot
    var3res.nglFrame        =  False

    var3res.cnFillOn        =  True
    var3res.cnFillMode      = 'AreaFill' #cell filling typ5
    var3res.cnLineLabelsOn = False

    var3res.cnLinesOn = False

    var3res.pmLabelBarDisplayMode = 'Never'

    cmap_colors = np.array([[0.5,0.64,0.65,0.4],[0.32,0.73,0.87,0.5],[0.33,0.34,0.93,0.6],[0.07,0.06,0.74,0.8],[0.6,0,0.6,1],
                            [0.6,0.01,0.07,1]])
    

    cmap_colors = np.insert(cmap_colors, 0, [0,0,0,0], axis=0)

    var3res.cnFillPalette    = cmap_colors #-- set the0 colormap to be used or 'NCL_default'

    var3res.cnLevelSelectionMode = "ExplicitLevels"
    var3res.cnLevels             =[1,2,3,4,6,12,24]# [ 1.5, 4, 6, 12, 24, 10**6]
    #var3res.cnMinLevelValF       = 0.1
    #var3res.cnMaxLevelValF       = 1.01
    #var3res.cnLevelSpacingF      = 0.1
    var3res.cnFillOpacityF       = 0.85
    var3res.cnNoDataLabelString  = 'No Variable Data'
    var3res.cnConstFLabelString  = 'No Variable Data'

    var3res.lbOrientation            = "horizontal" #-- horizontal labelbar
    var3res.lbTitleString            = '~F34~0~F~C' #f1.variables[list(f1.variables.items())[0][0]].units
    var3res.pmLabelBarOrthogonalPosF = -0.05
    # var3res.pmLabelBarParallelPosF   = 0.25 #-- move labelbar upward
    var3res.lbLabelFontHeightF       = 0.008 #-- labelbar labe font size
    var3res.lbBoxMinorExtentF        = 0.12 #-- decrease height of
    # var3res.lbBoxLinesOn             = True
    var3res.lbTitleFontHeightF       = 0.008 #label title font height
    var3res.lbTitleOffsetF           = -0.40 #title distance from the label
    var3res.lbBoxEndCapStyle         = "TriangleBothEnds"
    var3res.sfXArray = lon3 # processing of longitudes arrays
    var3res.sfYArray = lat3 # processing of latitudes arrays



    txresfill                    = Ngl.Resources()
    txresfill.txFont = "weather1"
    txresfill.txFontHeightF = 0.03

    txres                    = Ngl.Resources()
    txres.txFont = "o_weather1"
    txres.txFontHeightF = 0.03
    txres.gsnMaximize = False
    txres.txFontThicknessF=7.5
    #---- Integration of Resources of BaseMap and Variables
    pmres                    = Ngl.Resources() #pmres = True
    pmres.gsMarkerIndex      = 1 #marker index
    pmres.gsMarkerColor      = 'red'
    pmres.gsMarkerSizeF      = 0.05 #marker size
    pmres.gsMarkerThicknessF = 40
    pmres.gsLineThicknessF   = 8. #lines thickness
    map     = Ngl.map(wks, mpres)


    # lnid = Ngl.add_polyline(wks, map, lon0, lat0, plres)
    plot1    = Ngl.contour(wks, clct, var1res) #gsn_csm_contour command
    plot2    = Ngl.contour(wks, pmsl, var2res) #gsn_csm_contour command
    if number>0:
        plot3    = Ngl.contour(wks, rain_instant, var3res) #gsn_csm_contour command
    #plot4 = Ngl.contour(wks, pmsl, var4res)  # gsn_csm_contour command


    #Ngl.add_polymarker(wks, plot2, 9.732, 52.376, pmres) #marker locations
    Ngl.overlay(map, plot1)
    if number>0:
        Ngl.overlay(map, plot3)
    Ngl.overlay(map, plot2)
    Ngl.add_polymarker(wks, plot2, 9.732, 52.376, pmres) #marker locations



    scale_tudes =80#80
    lon_new = np.linspace(-75, 75, num=scale_tudes)
    lat_new = np.linspace(5, 80, num=scale_tudes)
 
    df = pd.DataFrame(ww)
    xr_data = xr.Dataset(
        {"data": (("latitude", "longitude"), df.values)},
        coords={"latitude": lat4, "longitude": lon4}
    )
    xr_data= xr_data.reindex(latitude=lat_new, longitude=lon_new, method='nearest')
    wws = xr_data.to_dataframe()


    symbols = pd.read_csv(dir_origin +"/ressources/Data/wwfont.csv")
    symbols = symbols.fillna(9999)
    #print(symbols.iloc[0])
    for i in lat_new :
        for j in lon_new:
          
            ww_number =   int(wws["data"][i][j])
            ww_symbol = symbols.iloc[ww_number]["letter"]
            ww_font = symbols.iloc[ww_number]["font"]
            ww_colour = symbols.iloc[ww_number]["colour"]
            if ww_symbol!= 9999:
                text_res = Ngl.Resources()
                #text_res.txFontHeightF = 0.015  # Schriftgröße anpassen
                text_res.txFont = "o_weather1"
                text_res.txFontHeightF = 0.03
                text_res.gsnMaximize = False
                text_res.txFontThicknessF=7.5
                text_res.txFontColor =ww_colour
                #print("symbols ", ww_symbol)
                txt = Ngl.add_text(wks, plot2,ww_symbol , j, i,text_res)



    hour, weekday, datetime_object,delta = imuktools.dates_for_subtitles(vara, number, filenames,model)
    left_string_2   = 'Bodendruck, sign. Wetter(Modell), Bewoelkung, akkumulierter Niederschlag'# +' & '+ f2.variables['GP_P0_L100_GLL0'].attributes['long_name'] #model output info
    left_string   = 'ICON-Lauf: '+  datetime_object.strftime('%a %d.%m.%Y %H')  +" UTC" +" (+"+delta+"h)"#model output info
    center_string = ''  # center information bar
    # right_string_2 = 'Init: ' + str(initial_time)
    right_string = weekday.capitalize() + " " + str(hour) + " UTC"  # + vld_time #model time information
    imuktools.subtitles(wks, map, left_string, center_string, right_string, mpres, left_string_2)  # assigning to main map
    Ngl.draw(map)
    Ngl.frame(wks)
    Ngl.destroy(wks)
    print('modell_weather_' + filenames[number])
    # ---- Crop Graphics

    if number>0:
        levellist=list(var3res.cnLevels)
        #levellist.pop()
        #imuktools.legendgl(number, 'modell_weather_', 11, wkres.wkWidth, wkres.wkHeight, filenames, 0, "mm", dir_origin, resx)
    resx= 945
    imuktools.quadlegend(number, 'modell_weather_'+model+"_", 10, wkres.wkWidth, wkres.wkHeight, var3res.cnFillPalette, list(var3res.cnLevels), filenames, 0, "mm", dir_origin, resx, trans=True, title="Niederschlag",low=-10)

    #imuktools.quadlegend(number, 't2m_'+model, 10, wkres.wkWidth, wkres.wkHeight, cmap_colors, list(var2res.cnLevels), filenames, 0, "°C", dir_origin, resx, trans=False, title="Temperatur",low=-10)



    imuktools.crop_image(number, 'modell_weather_'+model+"_", wkres, resx, resy, filenames,square=True)

    print('\EU has finished at: ', datetime.utcnow().strftime('%Y-%m-%d  %H:%M:%S '), u'\u2714' )
    return

def main():
    global varap,varbp, varcp, vardp ,numbers, resxs ,resys ,dir_origins ,filenames, rain_parameters
    ##Parsing Variable Values
    parser = argparse.ArgumentParser()
    parser.add_argument('resx')  # 350
    parser.add_argument('resy')  #
    parser.add_argument('outputpath')
    parser.add_argument('inputpath')
    parser.add_argument('timerangestart')
    parser.add_argument('timerangestop')
    parser.add_argument('timerangestepsize')
    parser.add_argument('model')
    args = parser.parse_args()  # gv[480#210    #480
    resx = int(args.resx)
    resy = int(args.resy)
    dir_origin = args.inputpath
    dir_Produkt = args.outputpath
    model = args.model
    os.chdir(dir_Produkt)

    varnumber = 4
    vars = ["clct_mod", "pmsl", "tot_prec", "ww"]
    varlevel = ["single", "single", "single", "single"]
    timerange = np.arange(int(args.timerangestart), int(args.timerangestop),
                          int(args.timerangestepsize))  
    filenames = imuktools.filenames(timerange)
    print(dir_origin)
    variablepaths = imuktools.varnames(varnumber, vars,
                                     varlevel,
                                     dir_origin,
                                     filenames,model=model)  ##Getting every filepath in the directory like [[vara1,vara2],[varb1,varb2]]

    timestepnumber = len(variablepaths[0])


    rain_parameters=[]
    varap= variablepaths[0]
    varbp= variablepaths[1]
    varcp = variablepaths[2]
    vardp= variablepaths[3]
    print(variablepaths[3])
    numbers =[] #np.arange(0,len(timerange))
    resxs=[resx]*len(timerange)
    resys=[resy]*len(timerange)
    dir_origins= [dir_origin]*len(timerange)
    #filenamess= [filenames]*len(timerange)
    for i in range(0, len(timerange)):
        # print(variablepaths[0][i])
        if i == 0:
            rain_parameters.append(np.array([]))
        else:
            rain_parameters.append(variablepaths[2][i - 1])
        numbers.append(i)

    elements = list(zip(varap,varbp, varcp, vardp ,numbers, resxs ,resys ,dir_origins ,filenames, rain_parameters))
    print(elements)
    print(len(elements))
    for i in range(0,len(timerange)):
        picture(variablepaths[0][i],variablepaths[1][i],variablepaths[2][i],variablepaths[3][i], i, resx, resy, dir_origin,filenames,rain_parameters[i],model)
    return


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

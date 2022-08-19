#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 20:19:33 2021
@author: juniperus

Revised on 20 Nov 2021 14:00:00
@author: juniperus

IMUK/Hannover
"""
    
#---- calling for the necessary libraries
import os
import Nio, Ngl
import numpy as np
import warnings
from datetime import datetime, timedelta
from PIL import Image
import metpy.calc as mpcalc

#---- Preliminaries (1)

warnings.filterwarnings("ignore")
current_date = datetime.utcnow()
print("EU has started at: ", current_date.strftime('%Y-%m-%d  %H:%M:%S'))
current_yr = current_date.year
current_mo = current_date.month
current_day = current_date.day
yrmoday = current_date.strftime('%d/%m/%Y')

dir_origin = os.getcwd()
dir_Produkt = 'database/output/'
os.chdir(dir_Produkt)

#---- open files and read variables

dir_shp     = os.path.join( dir_origin+'/database/shp/')
fn_shp      = dir_shp + 'DEU/gadm36_DEU_1.shp'
f0 = Nio.open_file(os.path.join(dir_shp, fn_shp), "r")   # Open shapefile

lon0     = np.ravel(f0.variables["x"][:])
lat0      = np.ravel(f0.variables["y"][:])
segments = f0.variables["segments"]

dir         = os.path.join(dir_origin) #path of model output
fn1          = dir + '/database/input/icon/2022/8/2/00/t/850/outfile_merged_2022080200_000_004_850_T.grib2' #path name of model output
f1           = Nio.open_file(os.path.join(dir, fn1)) #model output definition

print(f1.variables.keys()) # list of the variables briefly
for i in f1.variables: # main features of the variables
    print(f1.variables[i].long_name, f1.variables[i].name, f1.variables[i].units, f1.variables[i].shape)
    
lon1 = f1.variables['lon_0'][:] - 360
lat1 = f1.variables['lat_0'][:]
temp850 = f1.variables['TMP_P0_L100_GLL0'][4,:,:] -273.15

dir         = os.path.join(dir_origin) #path of model output
fn2          = dir + '/database/input/icon/2022/8/2/00/fi/850/outfile_merged_2022080200_000_004_850_FI.grib2' #path name of model output
f2           = Nio.open_file(os.path.join(dir, fn2)) #model output definition

print(f2.variables.keys()) # list of the variables briefly
for i in f2.variables: # main features of the variables
    print(f2.variables[i].long_name, f2.variables[i].name, f2.variables[i].units, f2.variables[i].shape)
    
lon2 = f2.variables['lon_0'][:] - 360
lat2 = f2.variables['lat_0'][:]
gph850 = f2.variables['GP_P0_L100_GLL0'][4,:,:] /98.1


'''fatal:NclGRIB2: Deleting reference to parameter; unable to decode grid template 3.101'''
'''see: https://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_temp3-101.shtml'''
'''see: https://www.dwd.de/DE/leistungen/opendata/help/modelle/Opendata_cdo_EN.pdf;jsessionid=F701F7DD8FE2D5E7E6AF606CB877DA9C.live11043?__blob=publicationFile&v=3'''


#---- Preliminaries (2)

temp850 = mpcalc.smooth_n_point(temp850, 9, 4)
gph850 = mpcalc.smooth_n_point(gph850, 9, 4)

#---- Initial Time

variable_name = [var for var in f1.variables.keys() if "TMP_P0_L100_GLL0" in var][0]
init_time = f1.variables[variable_name].attributes['initial_time']
init_time = init_time.split('/')
init_time[2] = init_time[2].split('(')
init_time_hr = init_time[2][1][:-4]
init_time_day = init_time[1]
init_time_mo = init_time[0]
init_time_yr = init_time[2][0]
initial_date = datetime(int(init_time_yr), int(init_time_mo), int(init_time_day), int(init_time_hr))
initial_time = initial_date.strftime('%d/%m/%Y %H') +'Z'

# #---- Valid Time

# vld_time_residual = int(f1.variables['TMP_P0_L100_GLL0'].attributes['forecast_time'] /60)
# vld_time = initial_date + timedelta(hours=vld_time_residual)
# vld_time = vld_time.strftime('%d/%m/%Y %H') + 'UTC'

#---- Designing a workstation
        
wkres           =  Ngl.Resources()                  #-- generate an resources object for workstation
wkres.wkBackgroundColor = 'black'
wkres.wkForegroundColor = 'white'
wkres.wkWidth   = 3840                             #-- width of workstation
wkres.wkHeight  = 2560                             #-- height of workstation
wks_type        = "png"                             #-- output type of workstation
wks             =  Ngl.open_wks(wks_type,'gph_temp_850', wkres)  #-- open workstation


#---- Resources

#---- Shapefile Resources

plres                  = Ngl.Resources()       # resources for polylines
plres.gsLineColor      = "black"
plres.gsLineThicknessF = 0                 # default is 1.0
plres.gsSegments       = segments[:,0] #province borders
# plres.sfXArray = lon0 # processing of longitudes arrays
# plres.sfYArray = lat0 # processing of latitudes arrays

#---- Basemap Resources

mpres = Ngl.Resources() 
mpres.nglMaximize       = True #expanding the draw
mpres.nglDraw           = False #-- don't draw plot
mpres.nglFrame          = False #-- don't advance frame
# mpres.mpShapeMode = "FreeAspect"
# mpres.vpWidthF = 5
# mpres.vpHeightF = 15
#mpres.tfDoNDCOverlay   = True 

mpres.mpPerimOn    = True
mpres.mpPerimLineThicknessF = 4.

mpres.mpOutlineOn                   = True #-- turn on map outlines
mpres.mpGeophysicalLineColor        = "black" #boundary color
mpres.mpGeophysicalLineThicknessF   = 5.0  # -- line thickness of coastal bo1 minutrders
mpres.mpDataBaseVersion             = "MediumRes"  #Map resolution
mpres.mpDataResolution              = 'Finest' #Data resolution
mpres.mpDataSetName                 = "Earth..4"  # -- set map data base version

mpres.mpLimitMode = "LatLon" #-- limiting the map via lat/lon
mpres.mpMinLatF = 35 #min(lat1) #-- min latitude
mpres.mpMaxLatF = 62 #max(lat1) #-- max latitude
mpres.mpMinLonF = -45  #min(lon1) #-- min longitude
mpres.mpMaxLonF = 45 #max(lon1) #-- max longtitude

# Converting the Lambert Perspective Options 
mpres.mpProjection         = "LambertConformal" #projection type
mpres.mpLambertMeridianF   = 10 #(mpres.mpMinLonF + mpres.mpMaxLonF) / 2 #reference longitude
diff_lon = (mpres.mpMaxLonF-mpres.mpMinLonF)
diff_lat = (mpres.mpMaxLatF-mpres.mpMinLatF)
domain_area = diff_lon*diff_lat

'''
The coordinates contains Germany:
    5 E - 16 E 
    46 N - 56 N
''' 

mpres.mpFillOn               = True  # -- turn on fill for map areas.
mpres.mpLandFillColor        = "grey"  # -- fill color land -darkslategray
mpres.mpOceanFillColor       = 'white' # -- fill color ocean -black
mpres.mpInlandWaterFillColor = 'white'  # -- fill color inland water
mpres.mpAreaMaskingOn        = False
# mpres.mpMaskAreaSpecifiers   = 'Germany'

# mpres.mpLandFillColor        = "transparent"  # -- fill color land -darkslategray
# mpres.mpOceanFillColor       = np.array([0,0,0,0.58]) # -- fill color ocean -black
# mpres.mpInlandWaterFillColor = np.array([0,0,0,0.58])   # -- fill color inland water

mpres.mpOutlineBoundarySets  = "national"  # -- "or geophysical"
mpres.mpOutlineSpecifiers    = "NullArea"  # -- plot state boundaries
mpres.mpNationalLineThicknessF = 0
mpres.mpNationalLineColor      = 'grey'
mpres.mpProvincialLineColor    = "grey"
mpres.mpGeophysicalLineColor      = 'black'
mpres.mpGeophysicalLineThicknessF      = 2
# mpres.mpFillDrawOrder          = 'PreDraw' 

#mpres.GridSpacingF = 10
mpres.mpGridAndLimbOn = True
mpres.mpGridLineColor = 'black'
mpres.mpGridLineThicknessF = 5
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
# var1res.cnLineLabelsOn = False
# var1res.cnFillMode = not necessary
var1res.cnLevelFlags = 'LineAndLabel'
var1res.cnLinesOn = True
var1res.cnLineThicknessF = 7.5
var1res.cnLineColor = 'chocolate3'
var1res.cnLineLabelBackgroundColor = -1
var1res.cnLineLabelFontColor = 'chocolate3'
var1res.cnLineLabelsOn = True
var1res.cnLineLabelFontHeightF = 0.006
var1res.cnLineLabelPlacementMode = "constant"
var1res.cnInfoLabelOn = False
# var1res.cnConstFEnableFill = False
# var1res.cnConstFLabelOn = False
# var1res.cnSmoothingOn = True
# var1res.cnSmoothingDistanceF = 0.00125

# var1res.cnLineLabelInterval = 1

var1res.pmLabelBarDisplayMode = 'Never'
# var1res.cnFillPalette    = 'BlAqGrYeOrRe' #-- set the0 colormap to be used or 'NCL_default'

cmap_colors = Ngl.read_colormap_file("GMT_wysiwygcont")
cmap_colors = cmap_colors[:-12]
# cmap = np.delete(cmap, [1,5,11], axis=0)
# cmap_colors = np.insert(cmap_colors, 0, [0,0,0,0], axis=0)
# cmap = np.insert(cmap, 10, [0,0,0,0], axis=0)

# cmap_colors[1:6] + martin_colors[5:9]

# cmap_martin = ("(/0,0,0/)",
#                 "(/0,0,.2/)", "(/0,0,.4/)", "(/0,0,.6/)", "(/0,0,.8/)", "(/0,0,1/)",\
#                 "(/0,.3,1/)", "(/0,.45,1/)", "(/0,.6,1/)", "(/0,.8,1/)", "(/0,1,1/)",\
#                 "(/0,1,.85/)", "(/0,1,.7/)", "(/0,1,.4/)", "(/.4,1,.2/)", "(/.8,1,.4/)",\
#                 "(/1,1,.65/)", "(/1,1,.55/)", "(/1,1,.4/)", "(/1,1,.2/)", "(/1,1,0/)",\
#                 "(/1,.8,.2/)", "(/1,.7,0/)", "(/1,.6,0/)", "(/1,.4,.05/)", "(/1,.3,.1/)",\
#                 "(/1,0,0/)", "(/.85,0,0/)", "(/0.7,0,0/)", "(/.55,0,0/)", "(/.4,0,0/)",\
#                 "(/.25,0,0/)") #(R, G, B) Values
    

var1res.cnFillPalette    = cmap_colors #-- set the0 colormap to be used or 'NCL_default'

var1res.cnLevelSelectionMode = "ManualLevels"
# var1res.cnLevels             = [0.001, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]
var1res.cnMinLevelValF       = -30
var1res.cnMaxLevelValF       = 30
var1res.cnLevelSpacingF      = 2 
var1res.cnFillOpacityF       = 0.99
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
# var1res.lbLabelStride = 5

# var1res.lbPerimOn = True
# var1res.lbPerimFill = 'SolidFill'
# var1res.lbPerimFillColor = np.array([0,0,0,0.83])
# var1res.lbLabelOffsetF = 0.08

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
var2res.cnLineLabelBackgroundColor = -1
var2res.cnLineLabelFontColor = 'black'
var2res.cnLineLabelPlacementMode = "constant"
var2res.cnLineLabelsOn = True
var2res.cnInfoLabelOn = False
# var2res.cnConstFEnableFill = False
# var2res.cnConstFLabelOn = False
# var2res.cnSmoothingOn = True
# var2res.cnSmoothingDistanceF = 0.00125

# var2res.cnLineLabelInterval = 1

var2res.pmLabelBarDisplayMode = 'Never'

var2res.cnLevelSelectionMode = "ManualLevels"
# var2res.cnLevels             = [0.001, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]
var2res.cnMinLevelValF       = 52
var2res.cnMaxLevelValF       = 200
var2res.cnLevelSpacingF      = 4 
# var2res.cnConpackParams = [ "HLX:20, HLY:20" ]    

# var2res.cnFillOpacityF = 0.85
var2res.cnLowLabelsOn = True
var2res.cnHighLabelsOn = True
var2res.cnHighLabelString = "H"
var2res.cnLowLabelString = "T"
var2res.cnHighLabelFontColor = 'black'
var2res.cnLowLabelFontColor = 'black'
# var2res.cnLowLabelFontHeightF = 0.012 #larger L labels
# var2res.cnHighLabelFontHeightF = 0.020 #larger H labels
var2res.cnLowLabelBackgroundColor = -1
var2res.cnHighLabelBackgroundColor = -1

var2res.sfXArray = lon2 # processing of longitudes arrays
var2res.sfYArray = lat2 # processing of latitudes arrays

#---- Integration of Resources of BaseMap and Variables

pmres                    = Ngl.Resources() #pmres = True
pmres.gsMarkerIndex      = 1 #marker index
pmres.gsMarkerColor      = 'red'
pmres.gsMarkerSizeF      = 0.003 #marker size
pmres.gsMarkerThicknessF = 40
pmres.gsLineThicknessF   = 8. #lines thickness
map     = Ngl.map(wks, mpres)
# lnid = Ngl.add_polyline(wks, map, lon0, lat0, plres)
plot1    = Ngl.contour(wks, temp850, var1res) #gsn_csm_contour command
plot2    = Ngl.contour(wks, gph850, var2res) #gsn_csm_contour command
# Ngl.overlay(map, lnid)
Ngl.overlay(map, plot1)
Ngl.overlay(map, plot2)
Ngl.add_polymarker(wks, plot2, 9.732, 52.376, pmres) #marker locations

#---- Annotations and Markers

def subtitles(wks, map, left_string, center_string, right_string):
    ltres = Ngl.Resources()
    ctres = Ngl.Resources()
    rtres = Ngl.Resources()
    ltres.nglDraw = False  # Make sure string is just created, not drawn.
    ctres.nglDraw = False  # Make sure string is just created, not drawn.
    rtres.nglDraw = False  # Make sure string is just created, not drawn.
    # Retrieve font height of left axis string and use this to calculate
    # size of subtitles.
   
    font_height = Ngl.get_float(map.base, "tiXAxisFontHeightF")
    ltres.txFontHeightF = font_height * 0.24  # Slightly smaller
    rtres.txFontHeightF = font_height * 0.44  # Slightly smaller
    ctres.txFontHeightF = font_height * 1.717  # Slightly smaller
    #ttres.txFont = 'complex_roman'
    ltres.txFontThicknessF = 5
    rtres.txFontThicknessF = 5
    
    # ttres.txBackgroundFillColor = np.array([0,0,0,0.55])
    ctres.txBackgroundFillColor = np.array([1,1,1,0.1])
    #rtres.txBackgroundFillColor = "yellow"
    rtres.txFontColor = "red"
   
    # Set some some annotation resources to describe how close text
    # is to be attached to plot.
   
    amres = Ngl.Resources() #amres = True
    amres.amOrthogonalPosF = -0.70  # Top of plot plus a little extra
    # to stay off the border.
   
    # Create three strings to put at the top, using a slightly
    # smaller font height than the axis titles.
   
    if left_string != "":
     txidl = Ngl.text(wks, map, left_string, mpres.mpLambertMeridianF, 51., ltres)
   
     amres.amJust = "TopLeft"
     amres.amParallelPosF = -0.5  # Left-justified
     amres.amOrthogonalPosF = 0.56 #-0.55
     annoidl = Ngl.add_annotation(map, txidl, amres)
     
     if left_string != "":
      txidl = Ngl.text(wks, map, left_string_2, mpres.mpLambertMeridianF, 51., ltres)
    
      amres.amJust = "BottomLeft"
      amres.amParallelPosF = -0.5  # Left-justified
      amres.amOrthogonalPosF = 0.55 #-0.56
      annoidl = Ngl.add_annotation(map, txidl, amres)
   
    if center_string != "":
     txidc = Ngl.text(wks, map, center_string, mpres.mpLambertMeridianF, 51., ctres)
   
     amres.amJust = "TopCenter"
     amres.amParallelPosF = 0.0  # Centered
     amres.amOrthogonalPosF = 0.501 #-0.65
     annoidc = Ngl.add_annotation(map, txidc, amres)
   
    if right_string != "":
     txidr = Ngl.text(wks, map, right_string, mpres.mpLambertMeridianF, 51., rtres)
   
     amres.amJust = "TopRight"
     amres.amParallelPosF = 0.5  # Right-justifed
     amres.amOrthogonalPosF = 0.54 #-0.55
     annoidr = Ngl.add_annotation(map, txidr, amres)
     
    # if right_string != "":
    #  txidr = Ngl.text(wks, map, right_string_2, mpres.mpLambertMeridianF, 51., rtres)
   
    #  amres.amJust = "BottomRight"
    #  amres.amParallelPosF = 0.5  # Right-justifed
    #  amres.amOrthogonalPosF = 0.55 #-0.56
    #  annoidr = Ngl.add_annotation(map, txidr, amres)
     
    return
 
# pmres                    = Ngl.Resources() #pmres = True
# pmres.gsMarkerIndex      = 6 #marker index
# pmres.gsMarkerColor      = 'black'
# pmres.gsMarkerSizeF      = 0.003 #marker size
# pmres.gsMarkerThicknessF = 4.44
# pmres.gsLineThicknessF   = 8. #lines thickness

# marker_berlin            = Ngl.add_polymarker(wks, map, 13.405, 52.520, pmres) #marker locations
# marker_cologne           = Ngl.add_polymarker(wks, map, 6.960, 50.938, pmres) #marker locations
# marker_frankfurt         = Ngl.add_polymarker(wks, map, 8.682, 50.111, pmres) #marker locations
# marker_hamburg           = Ngl.add_polymarker(wks, map, 9.993, 53.551, pmres) #marker locations
# marker_hannover          = Ngl.add_polymarker(wks, map, 9.732, 52.376, pmres) #marker locations
# marker_munich            = Ngl.add_polymarker(wks, map, 11.582, 48.135, pmres) #marker locations
# marker_stuttgart         = Ngl.add_polymarker(wks, map, 9.183, 48.776, pmres) #marker locations

# txres                    = Ngl.Resources() #txres = True
# txres.txFontHeightF      = '0.0{}'.format(domain_area/5) #font height
# txres.txFontColor        = 'black'
# id_berlin                = Ngl.add_text(wks, map, 'Berlin', 13.405, 52.520+0.22, txres) #citys text locations
# id_cologne               = Ngl.add_text(wks, map, 'Cologne', 6.960, 50.938+0.22, txres) #citys text locations
# id_frankfurt             = Ngl.add_text(wks, map, 'Frankfurt', 8.682, 50.111+0.22, txres) #citys text locations
# id_hamburg               = Ngl.add_text(wks, map, 'Hamburg', 9.993, 53.551+0.22, txres) #citys text locations
# id_hannover              = Ngl.add_text(wks, map, 'Hannover', 9.732, 52.376+0.22, txres) #citys text locations
# id_munich                = Ngl.add_text(wks, map, 'Munich', 11.582, 48.135+0.22, txres) #citys text locations
# id_stuttgart             = Ngl.add_text(wks, map, 'Stuttgart', 9.183, 48.776+0.22, txres) #citys text locations

# annores                  = Ngl.Resources()
# annores.txFontHeightF    = '0.0{}'.format(domain_area/2)
# annores.txFontColor      = 'white'
# annores.txBackgroundFillColor = 'black'
# annotation               = Ngl.add_text(wks, map, 'O.K. Mihliardic', mpres.mpLambertMeridianF, mpres.mpMinLatF+(domain_area/100), annores) #citys text locations

left_string_2   = '850 hPa: ' + f1.variables['TMP_P0_L100_GLL0'].attributes['long_name'] +' & '+ f2.variables['GP_P0_L100_GLL0'].attributes['long_name'] #model output info
left_string   = 'ICON-Lauf: ' + 'Init: ' + str(initial_time) #model output info
center_string = '                                               ' #center information bar
#center_string = '' #center information bar
# right_string_2 = 'Init: ' + str(initial_time) 
right_string  = 'Valid: ' #+ vld_time #model time information
subtitles(wks, map, left_string, center_string, right_string) #assigning to main map


#---- Drawing Conclusion

Ngl.draw(map)
Ngl.frame(wks)
# Ngl.delete_wks(wks)
Ngl.destroy(wks)

#---- Crop Graphics 

# im = Image.open('temp.png', mode='r')
# left   = 1000
# top    = 300
# right  = wkres.wkWidth - left
# bottom = wkres.wkHeight - top
# im1 = im.crop((left, top, right, bottom)) 
# im1.save("temp.png", format='png')
# Ngl.destroy(wks)

# #---- Merge Logo

# input_1 = "/media/juniperus/SONY/imuk/database/imuk_logo_trans.png"    
# input_2 = '/media/juniperus/SONY/imuk/database/input/icon/temp.png'
# output  = input_2
# cmd = f"composite -geometry 233x198.5+2880+1700 {input_1} {input_2} {output}"
# os.system(cmd)

print('\EU has finished at: ', datetime.utcnow().strftime('%Y-%m-%d  %H:%M:%S '), u'\u2714' )

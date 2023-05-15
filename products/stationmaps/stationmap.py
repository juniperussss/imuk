from __future__ import print_function
import Ngl
import numpy
import sys
import pandas as pd
database= pd.read_csv('../../ressources/Data/metarsupp.csv')

lats=database["lat"].tolist()
lons=database["lon"].tolist()

imdat=database["wwletter"].tolist()

#---Open file for graphics
wks_type = "png"
wks = Ngl.open_wks(wks_type,"wmstnm03")
wkres = Ngl.Resources()  # -- generate an resources object for workstation
wkres.wkBackgroundColor = 'white'
wkres.wkForegroundColor = 'white'


# ---- Resources

# ---- Shapefile Resources

plres = Ngl.Resources()  # resources for polylines
plres.gsLineColor = "black"
plres.gsLineThicknessF = 0  # default is 1.0
#plres.gsSegments = segments[:, 0]  # province borders
# plres.sfXArray = lon0 # processing of longitudes arrays
# plres.sfYArray = lat0 # processing of latitudes arrays

# ---- Basemap Resources

mpres = Ngl.Resources()
mpres.nglMaximize = True  # expanding the draw
#mpres.nglDraw = False  # -- don't draw plot
mpres.nglFrame = False  # -- don't advance frame
# mpres.mpShapeMode = "FreeAspect"
# mpres.vpWidthF = 5
# mpres.vpHeightF = 15
# mpres.tfDoNDCOverlay   = True

mpres.mpPerimOn = True
mpres.mpPerimLineThicknessF = 4.

mpres.mpOutlineOn = True  # -- turn on map outlines
mpres.mpGeophysicalLineColor = "black"  # boundary color
#mpres.mpGeophysicalLineThicknessF = (resx / 1920) * 5.0  # -- line thickness of coastal bo1 minutrders
mpres.mpDataBaseVersion = "MediumRes"  # Map resolution
mpres.mpDataResolution = 'Finest'  # Data resolution
mpres.mpDataSetName = "Earth..4"  # -- set map data base version

mpres.mpLimitMode = "LatLon"  # -- limiting the map via lat/lon
mpres.mpMinLatF = 35  # min(lat1) #-- min latitude
mpres.mpMaxLatF = 70  # max(lat1) #-- max latitude
mpres.mpMinLonF = -20#-45  # min(lon1) #-- min longitude
mpres.mpMaxLonF = 50#045  # max(lon1) #-- max longtitude

# Converting the Lambert Perspective Options
mpres.mpProjection = "LambertConformal"  # projection type
mpres.mpLambertMeridianF = 10  # (mpres.mpMinLonF + mpres.mpMaxLonF) / 2 #reference longitude
diff_lon = (mpres.mpMaxLonF - mpres.mpMinLonF)
diff_lat = (mpres.mpMaxLatF - mpres.mpMinLatF)
domain_area = diff_lon * diff_lat

'''
The coordinates contains Germany:
    5 E - 16 E 
    46 N - 56 N
'''

mpres.mpFillOn = True  # -- turn on fill for map areas.
mpres.mpLandFillColor = "white"  # -- fill color land -darkslategray
mpres.mpOceanFillColor = 'grey'  # -- fill color ocean -black
mpres.mpInlandWaterFillColor = 'grey'  # -- fill color inland water
mpres.mpAreaMaskingOn = True
# mpres.mpMaskAreaSpecifiers   = 'Germany'

# mpres.mpLandFillColor        = "transparent"  # -- fill color land -darkslategray
# mpres.mpOceanFillColor       = np.array([0,0,0,0.58]) # -- fill color ocean -black
# mpres.mpInlandWaterFillColor = np.array([0,0,0,0.58])   # -- fill color inland water

mpres.mpOutlineBoundarySets = "national"  # -- "or geophysical"
mpres.mpOutlineSpecifiers = "conterminous us: states"  # -- plot state boundaries
mpres.mpNationalLineThicknessF = 0
mpres.mpNationalLineColor = 'black'
# mpres.mpFillDrawOrder          = 'PreDraw'

# mpres.GridSpacingF = 10
mpres.mpGridAndLimbOn = True
mpres.mpGridLineColor = 'black'
mpres.mpGridLatSpacingF = 10.  # -- grid spacing for latitude
mpres.mpGridLonSpacingF = 20.  # -- grid spacing for longitude
mpres.mpGridLineDashPattern = 3  # -- dash pattern for grid lines

mpres.tmXBLabelsOn = False
mpres.tmXTLabelsOn = False
mpres.tmYRLabelsOn = False
mpres.tmYLLabelsOn = False
mpres.tmXBBorderOn = False
mpres.tmXTBorderOn = False
mpres.tmYRBorderOn = False
mpres.tmYLBorderOn = False
mpres.tmXBOn = False
mpres.tmXTOn = False
mpres.tmYROn = False
mpres.tmYLOn = False
pmres = Ngl.Resources()  # pmres = True
pmres.gsMarkerIndex = 1  # marker index
pmres.gsMarkerColor = 'red'
pmres.gsMarkerSizeF = 0.003  # marker size
pmres.gsMarkerThicknessF = 40
pmres.gsLineThicknessF = 8.  # lines thickness
map = Ngl.map(wks, mpres)


Ngl.wmsetp("ezf",1)
#Ngl.wmsetp("wbc",0.20) #	Diameter of sky cover circle at base of wind barb, expressed as a fraction of the shaft length.
#Ngl.wmsetp("wbl",0.10) #Size of the text labels in the station model display, expressed as a fraction of the shaft length.
Ngl.wmsetp("wbs",0.025) #Length of wind barb full tick as a fraction of its shaft length.
#Ngl.wmsetp("wbt",0.35)
Ngl.wmstnm(wks,lats,lons,imdat)
#Ngl.overlay(map, plot1)
Ngl.frame(wks)
Ngl.end()
import os
import Nio, Ngl
import numpy as np
import warnings
from datetime import datetime
import metpy.calc as mpcalc
from metpy.units import units
import ressources.tools.imuktools as imuktools
import argparse
import numpy.ma as ma

###
def picture(vara,varb,rain_parameter, number, resx, resy, dir_origin,filenames,model,mode):
    warnings.filterwarnings("ignore")
    current_date = datetime.utcnow()
    print("EU has started at: ", current_date.strftime('%Y-%m-%d  %H:%M:%S'))


 

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

    print(f1.variables.keys()) # list of the variables briefly


    lon1 = f1.variables['lon_0'][:] - 360
    lat1 = f1.variables['lat_0'][:]
    #t2 = f1.variables['TMP_P0_L103_GLL0'][:, :]-273.15
    t3 = f1.variables['CAPE_P0_L1_GLL0'][:, :]#-273.15



    dir         = os.path.join(dir_origin) #path of model output
    fn3          = varb# dir + '/database/input/icon/2022/8/2/00/tot_prec/outfile_merged_2022080200_000_004_TOT_PREC.grib2' #path name of model output
    f3          = Nio.open_file(os.path.join(varb))#dir, fn3)) #model output definition

    
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


    # ---- Initial Time
    
    #Draw left map
    wkres           =  Ngl.Resources() 
    wkres.wkWidth   = 3*resx # 3840                             #-- width of workstation
    wkres.wkHeight  = 3*resx #3840#2560    
    wks_type = "png"
    wks = Ngl.open_wks(wks_type,"panel2_"+ filenames[number],wkres)

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
    mpres.mpMinLatF = 25  # min(lat1) #-- min latitude
    mpres.mpMaxLatF = 72  # max(lat1) #-- max latitude
    mpres.mpMinLonF = -3 # min(lon1) #-- min longitude
    mpres.mpMaxLonF = 21  # max(lon1) #-- max longtitude

    # Converting the Lambert Perspective Options
    mpres.mpProjection         = "LambertConformal" #projection type
    mpres.mpLambertMeridianF   = 10 #(mpres.mpMinLonF + mpres.mpMaxLonF) / 2 #reference longitude
    diff_lon = (mpres.mpMaxLonF-mpres.mpMinLonF)
    diff_lat = (mpres.mpMaxLatF-mpres.mpMinLatF)
    domain_area = diff_lon*diff_lat



    mpres.mpFillOn               = True  # -- turn on fill for map areas.
    mpres.mpLandFillColor        = "#c4c38f"#"darkgreen"  # -- fill color land -darkslategray
    mpres.mpOceanFillColor       = "#95a69a"#'navy' # -- fill color ocean -black
    mpres.mpInlandWaterFillColor = "#95a69a"#'navy'  # -- fill color inland water
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



   
    #map = Ngl.map(wks, mpres)
    #plot2 = Ngl.contour(wks, t2, var2res)  # gsn_csm_contour command
    #Ngl.overlay(map, plot2)
    #Ngl.add_polymarker(wks, plot2, 9.732, 52.376, pmres) #marker locations
        # Temperaturwerte an jedem Gitterpunkt anzeigen

    var2res          = Ngl.Resources()
    var2res.nglDraw  = False
    var2res.nglFrame = False

    #
    # Loop through the timesteps and create each plot, titling each
    # one according to which timestep it is.
    #
    plot = []
    var2res.cnFillOn            = True    # Turn on contour fill.
    var2res.cnFillPalette       = "MPL_viridis"
    var2res.cnLineLabelsOn      = False   # Turn off contour labels

    #
    # Set some font heights to make them slightly bigger than the default.
    # Turn off nglScale, because this resource wants to set the axes font
    # heights for you.
    #
    var2res.nglScale               = False
    var2res.tiMainFontHeightF      = 0.037
    var2res.lbLabelFontHeightF     = 0.032
    var2res.tmXBLabelFontHeightF   = 0.030
    var2res.tmYLLabelFontHeightF   = 0.030


    var2res = Ngl.Resources()
    var2res.nglDraw = False  # -- don't draw plot
    var2res.nglFrame = False

    var2res.cnFillOn = True
    var2res.cnFillMode = 'AreaFill'  # cell filling typ5
    var2res.cnLineColor = 'transparent'
    var2res.cnLineLabelBackgroundColor = -1
    var2res.cnLineLabelFontColor = 'transparent'

    var2res.cnInfoLabelOn = False

    var2res.pmLabelBarDisplayMode = 'Never'
    colors = [
        [0, 0, 0],                  # Schwarz
        [46, 230, 46],              # Weniger gesättigtes Grün
        [23, 115, 23],              # Weniger gesättigtes Grün
        [230, 230, 0],              # Weniger gesättigtes Gelbgrün
        [230, 153, 0],              # Weniger gesättigtes Dunkelgelb
        [230, 79, 0],               # Weniger gesättigtes Orange
        [230, 0, 0],                # Weniger gesättigtes Hellorange
        [230, 46, 184],             # Weniger gesättigtes Dunkelrot
        [230, 0, 230],              # Weniger gesättigtes Rot
    ]




    # Transparenz für jede Farbe
    alphas = [0,1, 1, 1, 1, 1, 1, 1,1]

    # Kombination von Farben und Transparenz
    cmap_colors = np.column_stack((np.array(colors) / 255, alphas))

    #cmap_colors = np.array([[0.133, 0.588, 0.788, 1], [0.247, 0.690, 0.031, 1], [0.839, 0.812, 0.251, 1], [0.808, 0.475, 0.157, 1]])

    var2res.cnFillPalette = cmap_colors  # -- set the0 colormap to be used or 'NCL_default'

    var2res.cnLevelSelectionMode = "ExplicitLevels"
    var2res.cnLevels = [1,100,500,1000,1500,3000,3500,4000,4500,5000 ]# [ 1.5, 4, 6, 12, 24, 10**6]
    var2res.cnFillOpacityF = 0.99
    var2res.cnNoDataLabelString = 'No Variable Data'
    var2res.cnConstFLabelString = 'No Variable Data'

    var2res.lbOrientation = "horizontal"  # -- horizontal labelbar
    var2res.lbTitleString = '~F34~0~F~C'  # f1.variables[list(f1.variables.items())[0][0]].units
    var2res.pmLabelBarOrthogonalPosF = -0.05
    # var2res.pmLabelBarParallelPosF   = 0.25 #-- move labelbar upward
    var2res.lbLabelFontHeightF = 0.008  # -- labelbar labe font size
    var2res.lbBoxMinorExtentF = 0.12  # -- decrease height of
    # var2res.lbBoxLinesOn             = True
    var2res.lbTitleFontHeightF = 0.008  # label title font height
    var2res.lbTitleOffsetF = -0.40  # title distance from the label
    var2res.lbBoxEndCapStyle = "TriangleBothEnds"

    var2res.sfXArray = lon1  # processing of longitudes arrays
    var2res.sfYArray = lat1  # processing of latitudes arrays


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

#    for i in range(0,2):
 #<       plot.append(Ngl.contour(wks,t2,resources))
    map = Ngl.map(wks, mpres)
    plot1 =Ngl.contour(wks,t3,var2res) 
    Ngl.overlay(map, plot1)
    plot.append(map)

    map2 = Ngl.map(wks, mpres)
    plot2 =Ngl.contour(wks,rain_instant,var3res) 
    Ngl.overlay(map2, plot2)
    plot.append(map2)


    hour, weekday, datetime_object,delta = imuktools.dates_for_subtitles(vara, number, filenames,model)
    left_string_2   = 'Bodendruck, sign. Wetter(Modell), Bewoelkung, akkumulierter Niederschlag'# +' & '+ f2.variables['GP_P0_L100_GLL0'].attributes['long_name'] #model output info
    left_string   = 'ICON-Lauf: '+  datetime_object.strftime('%a %d.%m.%Y %H')  +" UTC" +" (+"+delta+"h)"#model output info
    center_string = ''  # center information bar
    # right_string_2 = 'Init: ' + str(initial_time)
    right_string = weekday.capitalize() + " " + str(hour) + " UTC"  # + vld_time #model time information
    #imuktools.subtitles(wks, map2, left_string, center_string, right_string, mpres, left_string_2)  # assigning to main map
    panel = Ngl.panel(wks,plot,[1,2])

    Ngl.end()
    
    #imuktools.crop_image(number, "panel2_", wkres, resx, resy, filenames,square=True)
    imuktools.crop_legend(number, "panel2_", wkres, resx, resy, filenames,dir_origin,datetime_object,model,var2res.cnFillPalette,var2res.cnLevels,var3res.cnFillPalette,var3res.cnLevels,square=True,mode=mode)
    #imuktools.crop_legend(number,levelname,wkres,resx,resy,filenames,inputpath,date,model,colormap,levels1, square=True,mode="summer")
    
    
    print('\EU has finished at: ', datetime.utcnow().strftime('%Y-%m-%d  %H:%M:%S '), u'\u2714')
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('resx')  # 350
    parser.add_argument('resy')  #
    parser.add_argument('outputpath')
    parser.add_argument('inputpath')
    parser.add_argument('timerangestart')
    parser.add_argument('timerangestop')
    parser.add_argument('timerangestepsize')
    parser.add_argument("model")
    parser.add_argument("mode")
    args = parser.parse_args()  
    resx = int(int(args.resx)/1)
    resy = int(args.resy)
    dir_origin = args.inputpath
    dir_Produkt = args.outputpath
    model =args.model
    mode = args.mode
    os.chdir(dir_Produkt)

    varnumber = 2
    vars = ["cape_con","tot_prec"]
    varlevel = ["single","single"]
    timerange = np.arange(int(args.timerangestart),int(args.timerangestop),int(args.timerangestepsize))#[0,3,6,9,180]# np.arange(0,12,3)
    filenames= imuktools.filenames(timerange)
    variablepaths = imuktools.varnames(varnumber, vars,
                                     varlevel,
                                     dir_origin, filenames,model)  ##Getting every filepath in the directory like [[vara1,vara2],[varb1,varb2]]

    timestepnumber = len(variablepaths[0])
    rain_parameters=[]
    for i in range(0, len(timerange)):
        print(variablepaths[1])
        if i == 0:
            rain_parameters.append(np.array([]))
        else:
            rain_parameters.append(variablepaths[1][i - 1])


    ## Main Process
    for i in range(0,len(timerange)):
        picture(variablepaths[0][i],variablepaths[1][i],rain_parameters[i], i, resx, resy, dir_origin,filenames,model,mode)
    return


if __name__ == "__main__":
    main()

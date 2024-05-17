import os
import Nio, Ngl
import numpy as np
import warnings
from datetime import datetime
import metpy.calc as mpcalc
from metpy.units import units
import ressources.tools.imuktools as imuktools
import argparse


###
def picture(vara, varb, number, resx, resy, dir_origin,filenames, model):
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

    print(f1.variables.keys()) # list of the variables briefly


    lon1 = f1.variables['lon_0'][:] - 360
    lat1 = f1.variables['lat_0'][:]
    u = f1.variables['UGRD_P0_L103_GLL0'][:, :]

    dir = os.path.join(dir_origin)  # path of model output
    fn2 = varb  # '/database/input/icon/2022/8/19/00/v/300/outfile_merged_2022081900_000_004_300_V.grib2' #path name of model output
    f2 = Nio.open_file(os.path.join(varb))  # model output definition


    lon2 = f2.variables['lon_0'][:] - 360
    lat2 = f2.variables['lat_0'][:]
    v = f2.variables['VGRD_P0_L103_GLL0'][:, :]


    # ---- Preliminaries (2)

    u = mpcalc.smooth_n_point(u, 9, 4)
    v = mpcalc.smooth_n_point(v, 9, 4)

    windspeed = mpcalc.wind_speed(np.array(u) * units('m/s'), np.array(v) * units('m/s'))
    windspeed_smoothed = mpcalc.smooth_n_point(windspeed, 9, 4)

    # ---- Initial Time

    variable_name = [var for var in f1.variables.keys() if "UGRD_P0_L103_GLL0" in var][0]
    init_time = f1.variables[variable_name].attributes['initial_time']
    init_time = init_time.split('/')
    init_time[2] = init_time[2].split('(')
    init_time_hr = init_time[2][1][:-4]
    init_time_day = init_time[1]
    init_time_mo = init_time[0]
    init_time_yr = init_time[2][0]
    initial_date = datetime(int(init_time_yr), int(init_time_mo), int(init_time_day), int(init_time_hr))
    initial_time = initial_date.strftime('%d/%m/%Y %H') + 'Z'

    # #---- Valid Time


    # ---- Designing a workstation
    aspect_ratio = resx / resy
    # print(10 *aspect_ratio, 10*resy/resx)
    wkres = Ngl.Resources()  # -- generate an resources object for workstation
    wkres.wkBackgroundColor = 'white'
    wkres.wkForegroundColor = 'white'
    wkres.wkWidth = 3 * resx  # 0.081*3840#299#0.081*3840  # -- width of workstation
    wkres.wkHeight = 3 * resx  # 0.081*3840#224#0.081*3840#2560  # -- height of workstation
    wks_type = "png"  # -- output type of workstation
    wks = Ngl.open_wks(wks_type, 'modell_wind_' + model+filenames[number], wkres)  # -- open workstation

    # ---- Resources

    # ---- Shapefile Resources

    plres = Ngl.Resources()  # resources for polylines
    plres.gsLineColor = "black"
    plres.gsLineThicknessF = 2.0  # default is 1.0
    plres.gsSegments = segments[:, 0]  # province borders


    mpres = Ngl.Resources()
    mpres.nglMaximize = True  # expanding the draw
    mpres.nglDraw = False  # -- don't draw plot
    mpres.nglFrame = False  # -- don't advance frame


    mpres.mpPerimOn = True
    mpres.mpPerimLineThicknessF = 4.

    mpres.mpOutlineOn = True  # -- turn on map outlines
    mpres.mpGeophysicalLineColor = "black"  # boundary color
    mpres.mpGeophysicalLineThicknessF = (resx / 1920) * 5.0  # -- line thickness of coastal bo1 minutrders
    mpres.mpDataBaseVersion = "MediumRes"  # Map resolution
    mpres.mpDataResolution = 'Finest'  # Data resolution
    mpres.mpDataSetName = "Earth..4"  # -- set map data base version

    mpres.mpLimitMode = "LatLon"  # -- limiting the map via lat/lon
    mpres.mpMinLatF = 37  # min(lat1) #-- min latitude
    mpres.mpMaxLatF = 60  # max(lat1) #-- max latitude
    mpres.mpMinLonF = -8 # min(lon1) #-- min longitude
    mpres.mpMaxLonF = 25  # max(lon1) #-- max longtitude

    # Converting the Lambert Perspective Options
    mpres.mpProjection = "LambertConformal"  # projection type
    mpres.mpLambertMeridianF = 10  # (mpres.mpMinLonF + mpres.mpMaxLonF) / 2 #reference longitude
    diff_lon = (mpres.mpMaxLonF - mpres.mpMinLonF)
    diff_lat = (mpres.mpMaxLatF - mpres.mpMinLatF)
    domain_area = diff_lon * diff_lat

    mpres.mpFillOn = True  # -- turn on fill for map areas.
    mpres.mpLandFillColor = "white"  # -- fill color land -darkslategray
    mpres.mpOceanFillColor = 'grey'  # -- fill color ocean -black
    mpres.mpInlandWaterFillColor = 'white'  # -- fill color inland water
    mpres.mpAreaMaskingOn = True


    mpres.mpOutlineBoundarySets = "national"  # -- "or geophysical"
    mpres.mpOutlineSpecifiers = "conterminous us: states"  # -- plot state boundaries
    mpres.mpNationalLineThicknessF = 4.0
    mpres.mpNationalLineColor = 'black'
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

    # ---- Variable (1) Resources

    var1res = Ngl.Resources()
    var1res.nglDraw = False  # -- don't draw plot
    var1res.nglFrame = False


    var1res.vcRefMagnitudeF = 1.  # make vectors larger
    var1res.vcRefLengthF = 0.018  # ref vec length
    var1res.vcGlyphStyle = "WindBarb"  # select wind barbs
    var1res.vcMinDistanceF = 0.023  # 0.048  # thin out windbarbs
    var1res.vcMonoWindBarbColor = True  # Turns multiple Windbarb colors on and off
    var1res.vcLevelColors = Ngl.read_colormap_file("ncl_default")
    var1res.vcGlyphOpacityF = 1
    var1res.vcWindBarbLineThicknessF = (resx / 1920) * 12
    var1res.vcWindBarbColor = "Black"
    var1res.vcWindBarbScaleFactorF = 1
    var1res.vcRefAnnoOn = False



    var1res.lbOrientation = "horizontal"  # -- horizontal labelbar
    var1res.lbTitleString = '~F34~0~F~C'  # f1.variables[list(f1.variables.items())[0][0]].units
    var1res.pmLabelBarOrthogonalPosF = -0.05
    # var1res.pmLabelBarParallelPosF   = 0.25 #-- move labelbar upward
    var1res.lbLabelFontHeightF = 0.008  # -- labelbar labe font size
    var1res.lbBoxMinorExtentF = 0.12  # -- decrease height of
    # var1res.lbBoxLinesOn             = True
    var1res.lbTitleFontHeightF = 0.008  # label title font height
    var1res.lbTitleOffsetF = -0.40  # title distance from the label
    var1res.lbBoxEndCapStyle = "TriangleBothEnds"
    # var1res.lbLabelStride = 5

    var1res.vfXArray = lon1  # processing of longitudes arrays
    var1res.vfYArray = lat1  # processing of latitudes arrays

    # ---- Variable (2) Resources

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

    # Liste von Farben
    colors = [
        [0, 0, 0],                  # Schwarz
        [45, 170, 0],               # Grün
        [144, 223, 0],              # Hellgrün
        [229, 220, 0],              # Gelb
        [230, 172, 38],             # Orange
        [220, 124, 33],             # Dunkelorange
        [213, 79, 26],              # Rotorange
        [210, 32, 30],              # Rot
        [194, 17, 60]               # Dunkelrot
    ]

    # Transparenz für jede Farbe
    alphas = [0, 1, 1, 1, 1, 1, 1, 1, 1]

    # Kombination von Farben und Transparenz
    cmap_colors = np.column_stack((np.array(colors) / 255, alphas))


    print(cmap_colors)
    #cmap_colors = np.array([np.array([0, 0, 0, 0]), [np.array([45, 170, 0])/255, 1], [np.array([144, 223, 0])/255, 1], [np.array([229, 220, 0])/255, 1], [np.array([230, 172, 38])/255, 1],[np.array([220, 124, 33])/255, 1],[np.array([213, 79, 26])/255, 1],[np.array([210, 32, 30])/255, 1], [np.array([194, 17, 60])/255, 1]])

    var2res.cnFillPalette = cmap_colors  # -- set the0 colormap to be used or 'NCL_default'

    var2res.cnLevelSelectionMode = "ExplicitLevels"
    var2res.cnLevels = [6, 11, 14,17, 21, 25,29 ,33]
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

    pmres                    = Ngl.Resources() #pmres = True
    pmres.gsMarkerIndex      = 1 #marker index
    pmres.gsMarkerColor      = 'red'
    pmres.gsMarkerSizeF      = 0.05 #marker size
    pmres.gsMarkerThicknessF = 40
    pmres.gsLineThicknessF   = 8. #lines thickness
    map = Ngl.map(wks, mpres)
    plot1 = Ngl.vector(wks, u, v, var1res)  # gsn_csm_contour command
    plot2 = Ngl.contour(wks, windspeed_smoothed, var2res)  # gsn_csm_contour command
    Ngl.overlay(map, plot2)
    Ngl.overlay(map, plot1)
    Ngl.add_polymarker(wks, plot2, 9.732, 52.376, pmres) #marker locations


    hour, weekday, datetime_object,delta = imuktools.dates_for_subtitles(vara, number, filenames, model =model)
    left_string_2 = '10 m  Wind (Fieder)' +' Boen, nach der Beaufortskala' # model output info
    left_string   = 'ICON-Lauf: '+  datetime_object.strftime('%a %d.%m.%Y %H')  +" UTC" +" (+"+delta+"h)"#model output info
    center_string = ''  # center information bar
    right_string = weekday.capitalize() + " " + str(hour) + " UTC"  # + vld_time #model time information
    imuktools.subtitles(wks, map, left_string, center_string, right_string, mpres, left_string_2)  # assigning to main map

    # Legends #
    def add_labelbar(wks, map, cmap):
        gsres = Ngl.Resources()  # Line resources.

        delta_lon = 4.0
        delta_lat = 2.1
        start_lon = -50
        start_lat = 40
        txres = Ngl.Resources()  # For labeling the label bar.
        txres.txFontHeightF = 0.015
        gid = []
        lid = []
        tid = []
        for i in range(4, 14, 1):
            lon0 = start_lon #+ (i - 4) * delta_lon
            lon1 = lon0 + delta_lon
            lat0 = start_lat + (i - 4) * delta_lat
            lat1 = start_lat + delta_lat
            lons = [lon0, lon1, lon1, lon0, lon0]
            lats = [lat0, lat0, lat1, lat1, lat0]
            gsres.gsFillColor = cmap[i - 4]  # Change fill color.
            gid.append(Ngl.add_polygon(wks, map, lons, lats, gsres))
            lid.append(Ngl.add_polyline(wks, map, lons, lats, gsres))
            if (i == 4):
                tid.append(Ngl.add_text(wks, map, "34.55", lon0, lat0 - delta_lat, txres))
            elif (i == 6):
                tid.append(Ngl.add_text(wks, map, "34.61", lon0, lat0 - delta_lat, txres))
            elif (i == 8):
                tid.append(Ngl.add_text(wks, map, "34.67", lon0, lat0 - delta_lat, txres))
            elif (i == 10):
                tid.append(Ngl.add_text(wks, map, "34.73", lon0, lat0 - delta_lat, txres))
            elif (i == 12):
                tid.append(Ngl.add_text(wks, map, "34.79", lon0, lat0 - delta_lat, txres))
            else:
                tid.append(Ngl.add_text(wks, map, "34.85", start_lon + 10 * delta_lon, lat0 - delta_lat, txres))

        return

    def labelbar(wks,map,cmap):
        gres = Ngl.Resources() #Line Ressources
        xstart = 0
        ystart = 0.1*wkres.wkHeight
        xend = 0.05*wkres.wkWidth
        yend =0.15*wkres.wkHeight
        lons = [lon0, lon1, lon1, lon0, lon0]
        lats = [lat0, lat0, lat1, lat1, lat0]
        xs=[xstart,xend,xend,xstart,xstart]
        ys=[ystart,ystart,yend,yend,ystart]
        gid=[]
        gres.gsFillColor = cmap[0]  # Change fill color.
        gid.append(Ngl.polygon(wks, xs, ys, gres))
    cmap = ["brown4", "yellow1", "navyblue", "forestgreen", "hotpink", "purple", \
            "slateblue", "thistle", "deeppink4", "darkgoldenrod"]

    Ngl.draw(map)
    Ngl.frame(wks)
    Ngl.destroy(wks)#

    imuktools.quadlegend(number, 'modell_wind_' + model, 10, wkres.wkWidth, wkres.wkHeight, cmap_colors, list(var2res.cnLevels), filenames, 0, "m/s", dir_origin, resx,title="Windboen")
    # ---- Crop Graphics
    imuktools.crop_image(number, 'modell_wind_' + model, wkres, resx, resy, filenames, square=True)
    # imuktools.crop_image_aspected(number,'u_v_300_',wkres,resx,resy)

    print('\EU has finished at: ', datetime.utcnow().strftime('%Y-%m-%d  %H:%M:%S '), u'\u2714')
    return


def main():
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
    print(args)
    resx = int(args.resx)
    resy = int(args.resy)
    dir_origin = args.inputpath
    dir_Produkt = args.outputpath
    os.chdir(dir_Produkt)
    model = args.model

    varnumber = 2
    vars = ["u_10m", "v_10m"]
    varlevel = ["single","single"]
    timerange = np.arange(int(args.timerangestart),int(args.timerangestop),int(args.timerangestepsize))#[0,3,6,9,180]# np.arange(0,12,3)
    filenames= imuktools.filenames(timerange)
    variablepaths = imuktools.varnames(varnumber, vars,
                                     varlevel,
                                     dir_origin, filenames, model=model)  ##Getting every filepath in the directory like [[vara1,vara2],[varb1,varb2]]

    timestepnumber = len(variablepaths[0])
    #print(variablepaths)

    ## Main Process
    for i in range(0,len(timerange)):
        #print(variablepaths[0][i])
        picture(variablepaths[0][i], variablepaths[1][i], i, resx, resy, dir_origin,filenames,model)
    return


if __name__ == "__main__":
    main()



  

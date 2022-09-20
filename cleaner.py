def cleaning_old_today_folders():
    import os
    import shutil
    from datetime import datetime, timedelta
    import glob
    today = datetime.now()
    filepath =  str(today.year) + "/" + str(today.month) + "/" + str(today.day)
    print(glob.glob(filepath + "/*"))
    filelist = glob.glob(filepath + "/*")
    oldday= today -timedelta(days=200)
    newfolder = 0
    print(len(filelist))
    deletelist = []
    if (len(filelist)==1):
        shutil.rmtree(os.getcwd() + "/" + filelist[0])
    else:
        for i in range(0, len(filelist)):
            oldfolder = newfolder
            newfolder = os.getcwd() + "/" + filelist[i]
            print(os.path.getmtime(newfolder))
            deletelist.append([os.path.getmtime(newfolder), i])
            if oldfolder < newfolder:
                print("removing", oldfolder)
                shutil.rmtree(oldfolder)

def archiving():
    import os
    import shutil
    import glob
    print(os.getcwd())
    filepath= os.getcwd()+"/database/output"
    folderlevel=["300","500","700","850","1000_gl"]
    dest= filepath +"/archiv/"
    shutil.rmtree(dest)
    os.mkdir(dest)
    for i in range(len(folderlevel)):
        src= filepath +"/"+folderlevel[i]
        desti= dest +"/" +folderlevel[i]
        shutil.copytree(src, desti, copy_function=shutil.copy)
    print("archiving successful")
    return





def varnames(varnumber,varnames,varlevel):
    from datetime import datetime
    import os
    import glob
    today = datetime.now()
    filepath = os.getcwd() + "/database/input/icon/" + str(today.year) + "/" + str(today.month) + "/" + str(today.day)
    initialtimefolder = glob.glob(filepath + "/*")[0]
    print("Initialtimefolder: ", initialtimefolder)
    varalist=[]
    for i in range(0,varnumber):
        varname = varnames[i]
        level = varlevel[i]
        if (level == "single"):
            varalist.append((glob.glob(initialtimefolder + "/" + varname + "/*")))
        else:
            varalist.append( (glob.glob(initialtimefolder + "/" + varname + "/" + str(level) + "/*")))

    print(varalist)
    return varalist


def cleaning_old_folders():
    from datetime import datetime
    import os
    import glob
    import shutil
    today = datetime.now()
    todaypath = os.getcwd() + "/database/input/icon/" + str(today.year) + "/" + str(today.month) + "/" + str(today.day)
    todayyearpath=os.getcwd() + "/database/input/icon/" + str(today.year)
    todaymonthpath=os.getcwd() + "/database/input/icon/" + str(today.year) + "/" + str(today.month)
    allyearpaths= glob.glob(os.getcwd() +"/database/input/icon/"+"/*")
    allmonthpaths=glob.glob(os.getcwd() + "/database/input/icon/" + str(today.year) + "/*")
    alldaypaths=glob.glob(os.getcwd() + "/database/input/icon/" + str(today.year) + "/" + str(today.month) + "/*" )
    print(allyearpaths)
    for i in range(len(allyearpaths)):
        if (allyearpaths[i] != todayyearpath):
            print("removing old year folders")
            shutil.rmtree(allyearpaths[i])
    for i in range(len(allmonthpaths)):
        if (allmonthpaths[i] != todaymonthpath):
            print("removing old Month folders")
            shutil.rmtree(allmonthpaths[i])
    for i in range(len(alldaypaths)):
        if (alldaypaths[i] != todaypath):
            print("removing old Day folders")
            shutil.rmtree(alldaypaths[i])
    return

def subtitles(wks, map, left_string, center_string, right_string,mpres,left_string_2):
        import Nio,Ngl
        import numpy as np
        ltres = Ngl.Resources()
        ctres = Ngl.Resources()
        rtres = Ngl.Resources()
        ltres.nglDraw = False  # Make sure string is just created, not drawn.
        ctres.nglDraw = False  # Make sure string is just created, not drawn.
        rtres.nglDraw = False  # Make sure string is just created, not drawn.
        # Retrieve font height of left axis string and use this to calculate
        # size of subtitles.

        font_height = Ngl.get_float(map.base, "tiXAxisFontHeightF")
        ltres.txFontHeightF = font_height * 0.4  # Slightly smaller
        rtres.txFontHeightF = font_height * 0.9  # Slightly smaller
        ctres.txFontHeightF = font_height * 1.717  # Slightly smaller
        # ttres.txFont = 'complex_roman'
        ltres.txFontThicknessF = 5
        rtres.txFont = 22

        # ttres.txBackgroundFillColor = np.array([0,0,0,0.55])
        ctres.txBackgroundFillColor = np.array([1, 1, 1, 0.1])
        rtres.txBackgroundFillColor = np.array([0, 1, 1, 1])
        ctres.txBackgroundFillColor = "white"
        rtres.txBackgroundFillColor = "yellow"
        rtres.txFontColor = "red"
        ltres.txFontColor = "blue"

        # Set some some annotation resources to describe how close text
        # is to be attached to plot.

        amres = Ngl.Resources()  # amres = True
        amres.amOrthogonalPosF = -0.70  # Top of plot plus a little extra
        # to stay off the border.

        # Create three strings to put at the top, using a slightly
        # smaller font height than the axis titles.

        if left_string != "":
            txidl = Ngl.text(wks, map, left_string, mpres.mpLambertMeridianF, 51., ltres)

            amres.amJust = "TopLeft"
            amres.amParallelPosF = -0.5  # Left-justified
            amres.amOrthogonalPosF = 0.56  # -0.55
            annoidl = Ngl.add_annotation(map, txidl, amres)

            if left_string != "":
                txidl = Ngl.text(wks, map, left_string_2, mpres.mpLambertMeridianF, 51., ltres)

                amres.amJust = "BottomLeft"
                amres.amParallelPosF = -0.5  # Left-justified
                amres.amOrthogonalPosF = 0.55  # -0.56
                annoidl = Ngl.add_annotation(map, txidl, amres)

        if center_string != "":
            txidc = Ngl.text(wks, map, center_string, mpres.mpLambertMeridianF, 51., ctres)

            amres.amJust = "TopCenter"
            amres.amParallelPosF = 0.0  # Centered
            amres.amOrthogonalPosF = 0.501  # -0.65
            annoidc = Ngl.add_annotation(map, txidc, amres)

        if right_string != "":
            txidr = Ngl.text(wks, map, right_string, mpres.mpLambertMeridianF, 51., rtres)

            amres.amJust = "TopRight"
            amres.amParallelPosF = 0.5  # Right-justifed
            amres.amOrthogonalPosF = 0.50  # -0.55
            annoidr = Ngl.add_annotation(map, txidr, amres)

        # if right_string != "":
        #  txidr = Ngl.text(wks, map, right_string_2, mpres.mpLambertMeridianF, 51., rtres)

        #  amres.amJust = "BottomRight"
        #  amres.amParallelPosF = 0.5  # Right-justifed
        #  amres.amOrthogonalPosF = 0.55 #-0.56
        #  annoidr = Ngl.add_annotation(map, txidr, amres)

        return

def dates_for_subtitles(vara,number):
    import os
    from datetime import datetime, timedelta
    strObj = os.path.basename(vara)  # Get Filestring
    strObj = strObj[6:16:]  # Cut to Datestring
    datetime_object = datetime.strptime(strObj, '%Y%m%d%H')  # Convert Datestring to Datetimeobject
    newdatetime_object = datetime_object + timedelta(hours=number * 3)
    weekday = newdatetime_object.strftime("%a")  # Extract Weekday from Datetimeobject
    hour = newdatetime_object.strftime("%H")
    return hour,weekday,datetime_object

def crop_image(number,levelname,wkres):
    from PIL import Image
    im = Image.open(levelname + str(number) + ".png", mode='r')
    left = 70
    top = 960
    right = wkres.wkWidth - 90
    bottom = wkres.wkWidth - 780
    im1 = im.crop((left, top, right, bottom))
    im1.save(levelname + str(number) + ".png", format='png')
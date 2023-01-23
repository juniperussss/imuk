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





def varnames(varnumber,varnames,varlevel,projectfolder,filenames):
    from datetime import datetime
    import os
    import glob
    import numpy as np
    #from cleaner import filenames
    today = datetime.now()
    filepath = projectfolder + "/database/input/icon/" + str(today.year) + "/" + str(today.month) + "/" + str(today.day)
    initialtimefolder = glob.glob(filepath + "/*")[0]
    print("inial:",initialtimefolder)
    varalist=[]
    varafilterdlist=[[] for _ in range(varnumber)]

    for i in range(0,varnumber):
        varname = varnames[i]
        level = varlevel[i]
        if (level == "single"):
            varalist.append((sorted(glob.glob(initialtimefolder + "/" + varname + "/*"))))
        else:
            varalist.append( (sorted(glob.glob(initialtimefolder + "/" + varname + "/" + str(level) + "/*"))))
        
    ## Filtering
    for h in filenames:
        for i in range(len(varalist)):
            for j in range(len(varalist[i])):

                if ('_'+h+'_' in varalist[i][j]) == True:
                    varafilterdlist[i].append(varalist[i][j])
    print(varafilterdlist)
    return varafilterdlist


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

def dates_for_subtitles(vara,number,filenames):
    import os
    from datetime import datetime, timedelta
    strObj = os.path.basename(vara)  # Get Filestring
    strObj = strObj[6:16:]  # Cut to Datestring
    datetime_object = datetime.strptime(strObj, '%Y%m%d%H')  # Convert Datestring to Datetimeobject
    # Check which timedelta needs to be used
    if number >0:
        oldtime =filenames[number-1]
        newtime = filenames[number]
    else:
        oldtime=0
        newtime = filenames[number]
    #print("num",number)
    deltatime=abs(int(oldtime)-int(newtime))
    #print(abs(int(oldtime)-int(newtime)))
    
    #tdatetime_object = datetime.strptime(tstrObj, '%Y%m%d%H') 
    fcst_hrs=filenames
    if len(fcst_hrs)>0:
        if number >0:
            deltatime=int(abs(int(fcst_hrs[number])-int(fcst_hrs[number-1])))
            #print("delta",deltatime, number, fcst_hrs[number])
        else:
            deltatime = 0
    else:
        deltatime=0
    newdatetime_object = datetime_object + timedelta(hours=number * deltatime)
    weekday = newdatetime_object.strftime("%a")  # Extract Weekday from Datetimeobject
    hour = newdatetime_object.strftime("%H")
    return hour,weekday,datetime_object

def crop_image(number,levelname,wkres,resx,resy,filenames):
    from PIL import Image
    import os
    im = Image.open(levelname +  filenames[number] + ".png", mode='r')
    left = wkres.wkWidth /55#70
    top = wkres.wkWidth/4 #4 #960
    right = wkres.wkWidth - wkres.wkWidth/43#90
    bottom = wkres.wkWidth - wkres.wkWidth/5#780
    im1 = im.crop((left, top, right, bottom))
    left = 0
    top = 0
    right = resx
    bottom =resy
    #im2 = im1.crop((left, top, right, bottom))
    im2 = im1.resize((resx, resy), resample=Image.BOX)
    im2.save(levelname + filenames[number] + ".jpg", format='jpeg')
    os.remove(levelname +  filenames[number] + ".png")

def crop_image_aspected(number,levelname,wkres,xres,yres):
    from PIL import Image
    im = Image.open(levelname + str(number) + ".png", mode='r')
    left = 0
    top = 0
    right = xres
    bottom =yres
    im1 = im.crop((left, top, right, bottom))
    im1.save(levelname + str(number) + ".jpg", format='jpg')


def fcst_hrsf():
    import numpy as np
    # fcst_hr_1 = np.arange(0, 78, 1)
    # fcst_hr_2 = np.arange(78, 181, 3)
    # fcst_hrs = np.concatenate((fcst_hr_1, fcst_hr_2))
    
    fcst_hrs = np.arange(0, 181, 3)
    #fcst_hrs = np.arange(0, 5, 1)
    #fcst_hrs= [0,12,36]
    
    return fcst_hrs
def filenames(timerange):
    #from cleaner import fcst_hrsf
    #fcst_hrs = fcst_hrsf()
    fcst_hrs_output = []
    for output in timerange:
        fcst_hrs_string = str(output).zfill(3)
        fcst_hrs_output.append(fcst_hrs_string)
    return fcst_hrs_output

def legendBACK(number,levelname,stepsize,width,heigth,colormap,levels,filenames,stepstart, unit):
    from PIL import Image, ImageDraw as D, ImageFont
    import numpy as np
    im = Image.open(levelname + filenames[number] + ".png", mode='r')
    left = 0
    top = 0
    xmin = 0.03*width
    xmax = 0.07*width
    ymin = 0.745*heigth
    ymax = 0.6*heigth
    shape= [(0.75*xmin,ymin),(2*xmax,ymax)]#
    shaper=[(100,100),(250,250)]
    draw = D.Draw(im)
    draw.rectangle(shape, fill="white")
    myFont=ImageFont.truetype('/ressources/fonts/liberation/LiberationSerif-Regular.ttf', 60)
    draw.text((1.05 * xmax, 0.99*ymax), unit, fill=(0, 0, 0), font=myFont)
    ylast= ymin
    ysteps= int(max(levels)/stepsize) +1 #How many Levels are needed
    ydelta = (ymin-ymax)/ysteps
   # colormap=["yellow","red","green","blue", "purple", "black","white","orange"]
    ci=0
    for i in range(stepstart,ysteps*stepsize-(2*ysteps),ysteps):
        ylow= ylast
        yhigh=ylow-ydelta
        #print(yhigh/heigth)
        shape=[(xmin,yhigh),(xmax,ylow)]
        fill = tuple(np.array(colormap[ci]*256).astype(int))
        draw = D.Draw(im)
        draw.rectangle(shape, fill=fill, outline="black", width=3)
        if ci < len(levels):
            draw.text((1.05*xmax, 0.99*yhigh), str(levels[ci]), fill = (0, 0, 0),font=myFont)
        ylast=yhigh
        ci +=1
    im.save(levelname + filenames[number] + ".png", format='png')
    #os.remove(levelname +  filenames[number] + ".png")


def legend(number,levelname,stepsize,width,heigth,colormap,levels,filenames,stepstart, unit,inputpath,resx):
    from PIL import Image, ImageDraw as D, ImageFont
    import numpy as np
    im = Image.open(levelname + filenames[number] + ".png", mode='r')
    ## Drawing the outer rectangle
    left = 0
    top = 0
    xmin = 0.03*width
    xmax = 0.07*width
    ymin = 0.745*heigth
    ymax = 0.6*heigth
    shape= [(0.75*xmin,1.01*ymin),(1.75*xmax,ymax)]#
    shaper=[(100,100),(250,250)]
    draw = D.Draw(im)
    fontsize= int( (resx/1920) *100)
    draw.rectangle(shape, fill="white")

    myFont=ImageFont.truetype(inputpath+'/ressources/fonts/liberation/LiberationSerif-Regular.ttf', fontsize)
    draw.text((1.45 * xmax, 0.99*ymax), unit, fill=(0, 0, 0), font=myFont)
    # Calculating inner rectangle
    ylast= ymin
    ysteps= int(max(levels)/stepsize) #+1 #How many Levels are needed
    ydelta = (ymin-ymax)/ysteps
    gesammtrange= ymin-ymax
    maxval= max(levels)
    ci=0
    outlinewidth=int( (resx/1920) *3)
    ##Drawing inner rectangles
    while ci< len(levels):
        if ci== 0:
            deltav= levels[ci]
        else:
            deltav= levels[ci] -levels[ci-1]
    # Calculating percentage
        anteil = deltav/maxval
        ylow= ylast
        yhigh=ylow-anteil*gesammtrange
        shape=[(xmin,yhigh),(xmax,ylow)]
        fill = tuple(np.array(colormap[ci]*256).astype(int))
        draw = D.Draw(im)
        draw.rectangle(shape, fill=fill, outline="black", width=outlinewidth)
        if str(colormap[ci]) == "[0. 0. 0. 0.]":
            print("yeah")
            xmintrans= xmin
            xmaxtrans= xmax
            ylowtrans = ylow
            yhightrans =yhigh
        if ci < len(levels) and levels[ci]%1< 0.5:
            #draw= D.Draw(im)
            #draw.rectangle(shape, fill=fill, outline="black", width=3)
            draw.text((1.05*xmax, 0.99*yhigh), str(levels[ci]), fill = (0, 0, 0),font=myFont)
        ylast=yhigh
        ci +=1
    
    #### Adding Fake Transparency ######
    imtrans = Image.open(inputpath+'/ressources/img/trans3.png', mode='r')
    xtransdelta= int(xmaxtrans-xmintrans)
    ytransdelta= int(abs(yhightrans-ylowtrans))
    resized = imtrans.resize((xtransdelta-outlinewidth,ytransdelta-2*outlinewidth))
    im.paste(resized, (int(xmintrans+outlinewidth),int(yhightrans+outlinewidth)))

    im.save(levelname + filenames[number] + ".png", format='png')
    #os.remove(levelname +  filenames[number] + ".png")

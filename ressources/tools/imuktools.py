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





def varnames(varnumber,varnames,varlevel,projectfolder,filenames,model="icon"):
    from datetime import datetime
    import os
    import glob
    import numpy as np
    #from cleaner import filenames
    today = datetime.now()
    filepath = projectfolder + "/database/input/"+model+"/" + str(today.year) + "/" + str(today.month) + "/" + str(today.day)
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

def dates_for_subtitles(vara,number,filenames, model="icon"):
    import os
    from datetime import datetime, timedelta
    import locale
    try:
        locale.setlocale(locale.LC_TIME, 'de_DE.UTF8')
    except:
        try:
            locale.setlocale(locale.LC_TIME, 'de_DE')
        except: 
            print("local could not been setr")
            pass

    #locale.setlocale(
     #   category=locale.LC_ALL,
      #  locale=""
    #)
    strObj = os.path.basename(vara)  # Get Filestring
    if model == "icon":
        strObj = strObj[6:16:]  # Cut to Datestring
    elif model == "icon-eu":
        strObj = strObj[44:54:]  # Cut to Datestring
    elif model == "icon-d2":
        strObj = strObj[45:55:]  # Cut to Datestring
    else:
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
    delta=str(number * deltatime).zfill(2)
    return hour,weekday,datetime_object,delta

def crop_image(number,levelname,wkres,resx,resy,filenames,square=False):
    from PIL import Image
    import os
    im = Image.open(levelname +  filenames[number] + ".png", mode='r')
    if square :
        lh=50
        th=8.9
        rh=40
        bh=80
    else:
        lh=55
        th=4
        rh=43
        bh=5
    left = wkres.wkWidth /lh
    top = wkres.wkWidth/th
    right = wkres.wkWidth - wkres.wkWidth/rh
    bottom = wkres.wkWidth - wkres.wkWidth/bh
    im1 = im.crop((left, top, right, bottom))
    left = 0
    top = 0
    right = resx
    bottom =resy
    im2 = im1.resize((resx, resy), resample=Image.LANCZOS)
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


def fcst_hrsf(model="icon"):
    import numpy as np
    if "eu" in model:
        f_range = 121
    elif "d2"in model:
        f_range = 51 
    else:
        f_range =  181

    fcst_hrs = np.arange(0, f_range, 3)
    
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


def legend(number,levelname,stepsize,width,heigth,colormap,levels,filenames,stepstart, unit,inputpath,resx,trans=True):
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
    if trans:
        imtrans = Image.open(inputpath+'/ressources/img/trans3.png', mode='r')
        xtransdelta= int(xmaxtrans-xmintrans)
        ytransdelta= int(abs(yhightrans-ylowtrans))
        resized = imtrans.resize((xtransdelta-outlinewidth,ytransdelta-2*outlinewidth))
        im.paste(resized, (int(xmintrans+outlinewidth),int(yhightrans+outlinewidth)))

    im.save(levelname + filenames[number] + ".png", format='png')
    #os.remove(levelname +  filenames[number] + ".png")


def legendgl(number, levelname, stepsize, width, heigth, filenames, stepstart, unit, inputpath, resx):
    from PIL import Image, ImageDraw as D, ImageFont
    import numpy as np

    colormap=np.array([[0,0,0,0],[0.5,0.64,0.65,0.4],[0.32,0.73,0.87,0.5],[0.33,0.34,0.93,0.6],[0.07,0.06,0.74,0.8],[0.6,0,0.6,1],[0.6,0.01,0.07,1],[1,0,0,1]])
    levels=list(["0.1-0.5","0.5-2","2-4","4-6","6-12","12-24",">24"])
    im = Image.open(levelname + filenames[number] + ".png", mode='r')
    ## Drawing the outer rectangle
    left = 0
    top = 0
    xmin = 0.03 * width
    xmax = 0.07 * width
    ymin = 0.74 * heigth
    ymax = 0.6 * heigth
    yminblue=1.01*0.61*heigth
    ymaxblue=0.6015*heigth
    xminblue=0.75*0.033* width
    xmaxblue=1.75*0.069*width
    shape = [(0.75 * xmin, 1.01 * ymin), (1.75 * xmax, ymax)]  #
    shaper = [( xminblue,  yminblue), (xmaxblue, ymaxblue)]
    draw = D.Draw(im)
    fontsize = int((resx / 1920) * 40)
    fontsizeblue= int((resx/1920)*40)
    #draw.rounded_rectangle(shape, radius=150,fill="blue")
    draw.rectangle(shape,fill="white",outline="black",width=7)
    draw.rectangle(shaper,fill="blue")
    myFont = ImageFont.truetype(inputpath + '/ressources/fonts/liberation/LiberationSerif-Regular.ttf', fontsize)
    bluefont= myFont = ImageFont.truetype(inputpath + '/ressources/fonts/liberation/LiberationSerif-Regular.ttf', fontsizeblue)

    #draw.text((1.45 * xmax, 0.99 * ymax), unit, fill=(0, 0, 0), font=myFont)
    draw.text((xmaxblue- 1.95*(1/2*abs(xminblue-xmaxblue)), ymaxblue-0.33*(1/2*abs(yminblue-ymaxblue))), "Regen 3h (mm)", fill=(255, 255, 255), font=bluefont)
    # Calculating inner rectangle
    ymax=0.62*heigth
    ylast = ymin
    ysteps = 7#int(max(levels) / stepsize)  # +1 #How many Levels are needed
    ydelta = (ymin - ymax) / ysteps
    gesammtrange = ( ymin - ymax)
    #maxval = max(levels)
    ci = 0
    outlinewidth = int((resx / 1920) * 3)
    ##Drawing inner rectangles
    while ci < len(levels):
        """
  
        if ci == 0:
            deltav = levels[ci]
        else:
            deltav = levels[ci] - levels[ci - 1]
              """
        # Calculating percentage
        anteil = 1/7
        ylow = ylast
        yhigh = ylow - anteil * gesammtrange
        shape = [(xmin, yhigh), (xmax, ylow)]
        fill = tuple(np.array(colormap[ci] * 256).astype(int))
        draw = D.Draw(im)
        draw.rectangle(shape, fill=fill, outline="black", width=outlinewidth)
        if str(colormap[ci]) == "[0. 0. 0. 0.]":
            #print("yeah")
            xmintrans = xmin
            xmaxtrans = xmax
            ylowtrans = ylow
            yhightrans = yhigh
       # if ci < len(levels) and levels[ci] % 1 < 0.5:
            # draw= D.Draw(im)
            # draw.rectangle(shape, fill=fill, outline="black", width=3)
        draw.text((1.05 * xmax, yhigh), str(levels[ci]), fill=(0, 0, 0), font=myFont) #(1/2* abs(ylow-yhigh))
        ylast = yhigh
        ci += 1

    #### Adding Fake Transparency ######
    imtrans = Image.open(inputpath + '/ressources/img/trans3.png', mode='r')
    xtransdelta = int(xmaxtrans - xmintrans)
    ytransdelta = int(abs(yhightrans - ylowtrans))
    resized = imtrans.resize((xtransdelta - outlinewidth, ytransdelta - 2 * outlinewidth))
    im.paste(resized, (int(xmintrans + outlinewidth), int(yhightrans + outlinewidth)))

    im.save(levelname + filenames[number] + ".png", format='png')
    # os.remove(levelname +  filenames[number] + ".png")


def quadlegend(number,levelname,stepsize,width,heigth,colormap,levels,filenames,stepstart, unit,inputpath,resx,trans=True, title="hans", low = 0):
    from PIL import Image, ImageDraw as D, ImageFont
    import numpy as np

    im = Image.open(levelname + filenames[number] + ".png", mode='r')
    ## Drawing the outer rectangle
    left = 0
    top = 0
    xmin = 0.03*width
    xmax = 0.08*width
    ymin = 0.9075*heigth
    ymax = 0.67*heigth
    shape= [(0.75*xmin,1.01*ymin),(1.75*xmax,0.9*ymax)]#
    shaper=[(100,100),(250,250)]
    draw = D.Draw(im)
    fontsize= int( (resx/1920) *100)
    print(fontsize)
    draw.rectangle(shape, fill="white",outline="black")

    myFont=ImageFont.truetype(inputpath+'/ressources/fonts/liberation/LiberationSerif-Regular.ttf', fontsize)
    title_font = ImageFont.truetype(inputpath+'/ressources/fonts/liberation/LiberationSerif-Bold.ttf', int(fontsize*1.2))
    # Calculating inner rectangle
    ylast= ymin
    ysteps= int(max(levels)/stepsize) #+1 #How many Levels are needed
    ydelta = (ymin-ymax)/ysteps
    gesammtrange= ymin-ymax
    maxval= max(levels)
    ci=0
    outlinewidth=int( (resx/1920) *3)
    # Drawing Title
    title_shape = [(0.78*xmin,0.95*ymax),(1.74*xmax,0.9*ymax)]
    draw = D.Draw(im)
    draw.rectangle(title_shape, fill=(0,0,255), outline="black", width=outlinewidth)
    draw.text((xmin, 0.91*ymax), title, fill = (255, 255, 255),font=title_font)

    draw.text((0.8 * xmax, 0.96*ymax), "("+unit+")", fill=(0, 0, 0), font=myFont)


    ##Drawing inner rectangles

    while ci< len(levels):
        if ci== 0:
            deltav= abs(levels[ci])
        else:
            deltav= levels[ci] - abs(levels[ci-1])
    # Calculating percentage
        anteil = 1/len(levels)#deltav/maxval
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

            draw.text((1.05*xmax, 0.99*yhigh), str(levels[ci]), fill = (0, 0, 0),font=myFont)
        ylast=yhigh
        ci +=1
    
    #### Adding Fake Transparency ######
    if trans:
        imtrans = Image.open(inputpath+'/ressources/img/trans3.png', mode='r')
        xtransdelta= int(xmaxtrans-xmintrans)
        ytransdelta= int(abs(yhightrans-ylowtrans))
        resized = imtrans.resize((xtransdelta-outlinewidth,ytransdelta-2*outlinewidth))
        im.paste(resized, (int(xmintrans+outlinewidth),int(yhightrans+outlinewidth)))

    im.save(levelname + filenames[number] + ".png", format='png')
    return

def metarww(metarstring):
    metarstring=metarstring.split(", ")[0]
    # Metarstring analysieren
    if metarstring == "patches of fog":
        ww = 41
    elif metarstring == "shallow fog":
        ww = 42
    elif metarstring == "partial fog":
        ww = 44
    elif metarstring == "fog":
        ww = 45
    elif metarstring == "freezing fog":
        ww = 49
    elif metarstring == "mist":
        ww = 10
    elif metarstring == "light drizzle":
        ww = 51
    elif metarstring == "drizzle":
        ww = 53
    elif metarstring == "heavy drizzle":
        ww = 53
    elif metarstring == "light drizle and rain":
        ww = 58
    elif metarstring == "light rain":
        ww = 61
    elif metarstring == "light freezing rain":
        ww = 66
    elif metarstring == "light rain and drizzle":
        ww = 58
    elif metarstring == "light rain and snow":
        ww = 68
    elif metarstring == "rain":
        ww = 63
    elif metarstring == "rain and snow":
        ww = 63
    elif metarstring == "light snow":
        ww = 71
    elif metarstring == "snow":
        ww = 75
    elif metarstring == "heavy snow":
        ww = 75
    elif metarstring == "light snow grains":
        ww = 77
    elif metarstring == "light ice pellets":
        ww = 79
    elif metarstring == "light rain showers":
        ww = 80
    elif metarstring == "rain showers":
        ww = 81
    elif metarstring == "light snow showers":
        ww = 85
    elif metarstring == "nearby showers":
        ww = 16
    elif metarstring == "light thunderstorm with rain":
        ww = 95
    elif metarstring == "thunderstorm":
        ww = 95
    elif metarstring == "thunderstorm with rain":
        ww = 95
    elif metarstring == "light thunderstorm with snow":
        ww = 95
    elif metarstring == "nearby thunderstorm":
        ww = 17
    elif metarstring == "unknown precipitation":
        ww = 0
    elif metarstring == "_":
        ww = 0


    return ww

def nclwwstring(dataframe):
    import pandas as pd
    import math
    data = dataframe
    #print(data.columns)
    letterlist=[]
    for x in data.index:
        #print(data.loc[x].visibility)
        ir= "1" #the precipitation data indicator?
        ix= "1" #weather data and station type indicator?
        h= "1" #height above ground of base of lowest cloud ?
        try:
            vv= str(int(0.00062137*data.loc[x].visibility.squeeze()))+ str(int(( data.loc[x].visibility.squeeze()% 1)*10)) #visibility in miles and fractions
        except:
            vv="00"
        try:
            N= str(int(data.loc[x].cloudcover.squeeze())) #total amount of cloud cover
        except:
            N="0"
        try:
            dd= str(int(data.loc[x].winddir.squeeze())).zfill(3)[0:2]#	direction from which wind is blowing
        except:
            dd="36"
        try:
            ff= str(int(data.loc[x].windspeed.squeeze())).zfill(2)##	wind speed in knots
        except:
            ff="00"
        ten='1'
        try:
            if math.copysign(1, data.loc[x].temperature.squeeze()) == -1:
                sn = "1"
            else:
                sn = "0"  # str(math.copysign(1, data[x].temperature.squeeze()))[0]
        except:
            sn="0"
        #sn= str(math.copysign(1,data[x].temperature.squeeze()))[0]
        try:
            ttt=str(abs(int(data.loc[x].temperature.squeeze()))).zfill(2) + str(int(( data.loc[x].temperature.squeeze()% 1)*10))
        except:
            ttt="000"
        fifteen= "2"
        try:
            if math.copysign(1, data.loc[x].dewpoint.squeeze()) == -1:
                snd= "1"
            else:
                snd = "0"# str(math.copysign(1, data[x].temperature.squeeze()))[0]
        except:
            snd="0"
        try:
            td = str(abs(int(data.loc[x].dewpoint.squeeze()))) + str(int((data.loc[x].temperature.squeeze() % 1) * 10))
        except:
            td="00"
        twenty="3"
        try:
            if len(str(int(data.loc[x].pressure.squeeze()))) >3:
                po=str(int(data.loc[x].pressure.squeeze()))[1:4] + str(int(( data.loc[x].pressure.squeeze()% 1)*10))
            else:
                po = str(int(data.loc[x].pressure.squeeze())) + str(int((data.loc[x].pressure.squeeze() % 1) * 10))
        except:
            po="0000"
        twentyfive = "4"
        try:
            if len(str(int(data.loc[x].sl_pressure.squeeze()))) > 3:
                pppp = str(int(data.loc[x].sl_pressure.squeeze()))[1:4] + str(int((data.loc[x].sl_pressure.squeeze() % 1) * 10))
            else:
                pppp = str(int(data.loc[x].sl_pressure.squeeze())) + str(int((data.loc[x].sl_pressure.squeeze() % 1) * 10))
        except:
            pppp="0000"

        thirty="5"
        a="1"
        try:
            ppp= str(abs(int(data.loc[x].pressure3h_change.squeeze()))).zfill(2)+str(int(( data.loc[x].pressure3h_change.squeeze()% 1)*10))
        except:
            ppp="000"
        thirtyfive="6"
        try:
            rrr= str(abs(int(data.loc[x].rain.squeeze()))).zfill(2)+str(int(( data.loc[x].rain.squeeze()% 1)*10))
        except:
            rrr="000"
        tr="0"
        fourty= "7"
        try:
            ww=str(abs(int(data.loc[x].weather.squeeze()))).zfill(2)
        except:
            ww="00"
        wone="0"
        wtwo="0"
        fourtyfive= "8"
        nh=N
        cl="0"
        cm="0"
        ch="0"
        wwletter= ir+ix+h+vv+N+dd+ff+ten+sn+ttt+fifteen+snd+td+twenty+po+twentyfive+pppp+thirty+a+ppp+thirtyfive+rrr+tr+fourty+ww+wone+wtwo+fourtyfive+nh+cl+cm+ch
        letterlist.append(wwletter)
    df = data.assign(wwletter=letterlist)
    return df
def pressurereduction(p,height,t):
    import math
    import numpy as np
    print(p, height, t)

    kappa=1.402
    M=0.02896
    g= 9.81
    r=8.314
    pmsl= np.round(p*(1-((kappa -1)/kappa) *((M*g*(-1*height))/(r*t)))**(kappa/(kappa -1)),2)
    print("hans")
    print("pmsl",pmsl)
    if pmsl <100: pmsl=pmsl+1000
    print("pmsl",pmsl)
    return pmsl

def calculate_sea_level_pressure(P_station, H_station, T_station):
    import numpy as np
    lapse_rate = 0.0065
    gravity = 9.807
    gas_constant = 287.0  # spezifische Gaskonstante für trockene Luft
    if P_station<100 : P_station=P_station+1000
    exponent = (gravity / (lapse_rate * gas_constant))
    try:
        sea_level_pressure = P_station * (1 + (lapse_rate * H_station) / (T_station + lapse_rate * H_station)) ** exponent
    except ZeroDivisionError:
        sea_level_pressure = 1000
    if np.real(sea_level_pressure)>9000: sea_level_pressure=sea_level_pressure/1000
    return sea_level_pressure
#def imdatconvert():
 #   precition_data_indicator = "a"

  #  imdat=

def cloudcover(obs):
    from metar import Metar
    from statistics import mean
    cc=[]
    for i in obs.sky:
    #print(i[0])
        if item[0] == "FEW":
            cc.append(1.5)
        elif item[0] == "NCS":
            cc.append(0)
        elif item[0] == "SCT":
            cc.append(3.5)
        elif item[0] == "BKN":
            cc.append(6)
        elif item[0] == "OVC":
            cc.append(8)
    return int(mean(cc))



def crop_legend(number,levelname,wkres,resx,resy,filenames,inputpath,date,model,colormap1,levels1,colormap2,levels2, square=True,mode="summer"):

    from PIL import Image, ImageDraw, ImageFont

    import os
    import numpy as np
    # Open the image
    im = Image.open(levelname + filenames[number] + ".png", mode='r')
    
    # Define crop dimensions
    if square:
        lh = 50
        th = 8.9
        rh = 40
        bh = 80
    else:
        # Define non-square crop dimensions if needed
        pass
    
    left = wkres.wkWidth / lh
    top = wkres.wkWidth / th
    right = wkres.wkWidth - wkres.wkWidth / rh
    bottom = wkres.wkWidth - wkres.wkWidth / bh
    
    # Crop the image
    im1 = im.crop((left, top, right, bottom))
    
    # Resize the cropped image
    im1_resized = im1.resize((int(resx-0), int(resy-80)), resample=Image.LANCZOS)
    
    # Create a new image (larger canvas)
    im2 = Image.new('RGB', (resx , resy ),color='white')  # Adjust dimensions as needed
    
    # Paste the resized image onto the new image as a layer
    im2.paste(im1_resized, (0, 0))  # Adjust position as needed


        # Draw a box on im2
    draw = ImageDraw.Draw(im2)
    box_width = 470  # Width of the box
    box_height = 40  # Height of the box
    box_color = 'white'  # Color of the box

    box_x = 0  # X-coordinate of the top-left corner of the box
    box_y = resy-105  # Y-coordinate of the top-left corner of the box

    font = ImageFont.truetype(inputpath+"/ressources/fonts/liberation/LiberationSerif-Regular.ttf", 20) 
    text_color = 'blue'  # Color of the text
    text = "CAPE (Flächen)"
    draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], fill=box_color,outline="black")
    draw.text((box_x + 10, box_y + 10), text, fill=text_color, font=font)
    print(mode)
    if mode == "summer":

        text = "Niederschlag akkumuliert (l/m^2)"

    else:
        text = "Schnee akkumuliert"
    box_x = 480  # X-coordinate of the top-left corner of the box
    draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], fill=box_color,outline="black")
    draw.text((box_x + 10, box_y + 10), text, fill=text_color, font=font)



    #Text large 
    font = ImageFont.truetype(inputpath+"/ressources/fonts/liberation/LiberationSerif-Regular.ttf", 25) 
    text = model.upper()+ "-Lauf "+ date.strftime("%a %d.%m.%Y %H:%M") + " Uhr"
    draw.text((0 + 10, resy -50), text, fill=text_color, font=font)

    # Yellow Box
    box_width = 270  # Width of the box
    box_height = 80  # Height of the box
    box_color = 'yellow'  # Color of the box

    box_x = resx-270  # X-coordinate of the top-left corner of the box
    box_y = resy-62  # Y-coordinate of the top-left corner of the box
    # Write text inside the box
    draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], fill=box_color,outline="black")
    text= date.strftime("%a %H") +" UTC"
    text_color = 'red'  # Color of the text
    font = ImageFont.truetype(inputpath+"/ressources/fonts/liberation/LiberationSerif-Bold.ttf", 50) 
    draw.text((resx-260 +10, resy -50), text, fill=text_color, font=font)
 # You may need to adjust the font and size

    #Legends

    #Legend1 
    box_width = 80  # Width of the box
    box_height = 290  # Height of the box
    box_color = 'white'  # Color of the box

    box_x = 1  # X-coordinate of the top-left corner of the box
    box_y = resy-398  # Y-coordinate of the top-left corner of the box


    draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], fill=box_color,outline="black")
    ymin = box_y+box_height-10
    ymax = box_height+270
    xmin = box_x +5
    xmax = box_x + box_width-38
    ylast= ymin
    #ysteps= int(max(levels1)/stepsize) #+1 #How many Levels are needed

    gesammtrange= ymin-ymax
    font = ImageFont.truetype(inputpath+"/ressources/fonts/liberation/LiberationSerif-Regular.ttf", 18) 
    ci=0
    print(levels1)
    while ci< len(levels1)-1:

    # Calculating percentage
        anteil = 1/len(levels1)#deltav/maxval
        ylow= ylast
        yhigh=ylow-anteil*gesammtrange
        shape=[(xmin,yhigh),(xmax,ylow)]
        fill = tuple(np.array(colormap1[ci]*256).astype(int))
        draw.rectangle(shape, fill=fill, outline="black", width=2)
        if str(colormap1[ci]) == "[0. 0. 0. 0.]":
            print("yeah")
            xmintrans= xmin
            xmaxtrans= xmax
            ylowtrans = ylow
            yhightrans =yhigh
        if ci < len(levels1) and levels1[ci]%1< 0.5:

            draw.text((1.05*xmax, 0.99*yhigh), str(levels1[ci]), fill = (0, 0, 0),font=font)
        ylast=yhigh
        ci +=1
        
    imtrans = Image.open(inputpath+'/ressources/img/trans3.png', mode='r')
        
    xtransdelta= int(xmaxtrans-xmintrans)
    ytransdelta= int(abs(yhightrans-ylowtrans))
    resized = imtrans.resize((xtransdelta-1,ytransdelta-2*1))
    im2.paste(resized, (int(xmintrans+1),int(yhightrans+1)))

    draw.text((xmax-22, 0.99*ymax), "j/kg", fill = (0, 0, 0),font=font)
    #Legend2
    box_x = resx-box_width-385  # X-coordinate of the top-left corner of the box
    box_y = resy-398  # Y-coordinate of the top-left corner of the box
    draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], fill=box_color,outline="black")
    ymin = box_y+box_height-10
    ymax = box_height+270
    xmin = box_x +5
    xmax = box_x + box_width-30
    ylast= ymin
    #ysteps= int(max(levels1)/stepsize) #+1 #How many Levels are needed

    gesammtrange= ymin-ymax

    ci=0
    print(levels2)
    while ci< len(levels2)-1:

    # Calculating percentage
        anteil = 1/len(levels2)#deltav/maxval
        ylow= ylast
        yhigh=ylow-anteil*gesammtrange
        shape=[(xmin,yhigh),(xmax,ylow)]
        fill = tuple(np.array(colormap2[ci]*256).astype(int))
        draw.rectangle(shape, fill=fill, outline="black", width=2)
        if str(colormap2[ci]) == "[0. 0. 0. 0.]":
            print("yeah")
            xmintrans= xmin
            xmaxtrans= xmax
            ylowtrans = ylow
            yhightrans =yhigh
        if ci < len(levels2) and levels2[ci]%1< 0.5:

            draw.text((1.02*xmax, 0.99*yhigh), str(levels2[ci]), fill = (0, 0, 0),font=font)
        ylast=yhigh
        ci +=1

    imtrans = Image.open(inputpath+'/ressources/img/trans3.png', mode='r')
        
    xtransdelta= int(xmaxtrans-xmintrans)
    ytransdelta= int(abs(yhightrans-ylowtrans))
    resized = imtrans.resize((xtransdelta-1,ytransdelta-2*1))
    im2.paste(resized, (int(xmintrans+1),int(yhightrans+1)))
    
    
    draw.text((xmax-30, 0.99*ymax), "l/m^2", fill = (0, 0, 0),font=font)
    # Save the result
    im2.save(levelname + filenames[number] + "_layered.jpg", format='JPEG')
    
    # Optionally, remove the original image
    os.remove(levelname + filenames[number] + ".png")

    return im2
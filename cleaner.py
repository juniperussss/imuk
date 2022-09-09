def cleaning_old_timefolders():
    import os
    import shutil
    from datetime import datetime, timedelta
    import glob
    today = datetime.now()
    filepath = "input/icon/" + str(today.year) + "/" + str(today.month) + "/" + str(today.day)
    print(glob.glob(filepath + "/*"))
    filelist = glob.glob(filepath + "/*")
    newfolder = 0
    print(len(filelist))
    deletelist = []
    for i in range(0, len(filelist)):
        oldfolder = newfolder
        newfolder = os.getcwd() + "/" + filelist[i]
        print(os.path.getmtime(newfolder))
        deletelist.append([os.path.getmtime(newfolder), i])
        if i > 0 and oldfolder < newfolder:
            print("removing", oldfolder)
            shutil.rmtree(oldfolder)

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
        varalist.append( (glob.glob(initialtimefolder + "/" + varname + "/" + str(level) + "/*")))

    print(varalist)
    return varalist
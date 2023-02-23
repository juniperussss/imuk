def metarrequest(dirorigin):

    from metar import Metar
    import pandas as pd
    import requests
    import airportsdata
    from tqdm import tqdm
    from cleaner import metarww, pressurereduction
    from datetime import datetime

    cdt_date = datetime.utcnow()
    cdt_yr = cdt_date.year
    cdt_mo = cdt_date.month
    cdt_day = cdt_date.day
    cdt_yrmoday = cdt_date.strftime('%Y%m%d')
    cdt_hour= cdt_date.hour

    if int(cdt_date.strftime("%H")) >= 4 and int(cdt_date.strftime("%H")) <= 11:
        init_time_hr = '00'
    elif int(cdt_date.strftime("%H")) >= 16 and int(cdt_date.strftime("%H")) <= 23:
        init_time_hr = '12'
    else:
        init_time_hr = '00'  # input('Enter the model run time ')
    #timedif= str(abs(int(init_time_hr)-cdt_hour)).zfill(2)
    #print(timedif)
    airports = airportsdata.load()  # key is the ICAO identifier (the default) # To get Coordinates from ICAO Codes
    response=requests.get("https://tgftp.nws.noaa.gov/data/observations/metar/cycles/"+init_time_hr+"Z.TXT")#+timedif+"Z.TXT")
    data = pd.read_csv(dirorigin+'/BUFR/airport_europe.csv') #Dataframe with all Stations of europe
    #print(airports["EBAM"]['elevation'])#['ETIC'])
    datawwfont = pd.read_csv(dirorigin+'/BUFR/wwfont.csv')  # Fontframe
    #print(datawwfont.iloc[4])
    listofairports=data['icao'].tolist()
    #print(listofairports)
    #data.head() # to display the first 5 lines of loaded data
    splitting = response.text.splitlines()
    temperature=[]
    weather=[]
    station=[]
    pressure=[]
    sl_pressure=[]
    dewpoint=[]
    time=[]
    windspeed=[]
    winddir=[]
    lon=[]
    lat=[]
    weatherfont=[]
    weathersymbol=[]
    weathercolour=[]
    #obsa=Metar.Metar("ETIC 031755Z AUTO 29011KT 9999 -RA FEW008 BKN012 BKN019 OVC026 06/05 A3010 RMK AO2 CIG 010V019 SLP205 P0003 60009 T00570047 10057 20049 53017")
    #print(obsa.trend())
    for i in tqdm(range(len(splitting))):
        #if "ED" in splitting[i] != False:
        #if splitting[i].startswith('ED'):# or splitting[i].startswith('ET'):
        if any(splitting[i].startswith(ele) for ele in listofairports):
            #weather.append(splitting[i])
            try:
                obs = Metar.Metar(splitting[i])
                weather.append(metarww(obs.present_weather()))
                weatherfont.append(datawwfont.iloc[metarww(obs.present_weather())]["font"])
                weathersymbol.append(datawwfont.iloc[metarww(obs.present_weather())]["letter"])
                weathercolour.append(datawwfont.iloc[metarww(obs.present_weather())]["colour"])
                station.append(obs.station_id)
                time.append(obs.time)
                lon.append(airports[obs.station_id]['lon'])
                lat.append(airports[obs.station_id]['lat'])
                try:
                    temperature.append(obs.temp.value())
                except AttributeError :
                    temperature.append(99999)
                try:

                    sl_pressure.append(pressurereduction(obs.press.value(),airports[obs.station_id]["elevation"],obs.temp.value()))
                    pressure.append(obs.press.value())
                except AttributeError :
                    pressure.append(99999)
                    sl_pressure.append(99999)

                try:
                    dewpoint.append(obs.dewpt.value())
                except AttributeError :
                    dewpoint.append(99999)

                try:
                    windspeed.append(obs.wind_speed.value())
                except AttributeError :
                    windspeed.append(99999)

                try:
                    winddir.append(obs.wind_dir.value())
                except AttributeError :
                    winddir.append(None)

            except (Metar.ParserError,UnboundLocalError,AttributeError) as err:
                #print("The following Error occurred", err)
                pass


    d = {"station":station, "lat":lat,"lon":lon,"time":time,"weather":weather, "weatherfont":weatherfont,"weathersymbol":weathersymbol,"weathercolour":weathercolour,"temperature":temperature,"pressure":pressure,"sl_pressure":sl_pressure,"dewpoint":dewpoint, "windspeed":windspeed, "winddir":winddir}

    df=pd.DataFrame(d)
    #metardata = df.loc[:, ~(df == '99999').any()]
    print(df.tail())

    duplicatedremove=df.drop_duplicates(subset=['station'], keep="last")
    print(duplicatedremove.tail())
    metar_csv_data = df.to_csv(dirorigin+'/BUFR/metardata.csv', index = True)
    metarcompare = duplicatedremove.to_csv(dirorigin+'/BUFR/metarcompare.csv', index = True)

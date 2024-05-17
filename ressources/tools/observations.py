def metarrequest(dirorigin):

    from metar import Metar
    import pandas as pd
    import requests
    import airportsdata
    from tqdm import tqdm

    from ressources.tools.imuktools import metarww, pressurereduction,cloudcover,nclwwstring,calculate_sea_level_pressure
    from datetime import datetime
    from datetime import timedelta
    from meteostat import Hourly
    from meteostat import Stations
    import json
    import warnings
    warnings.filterwarnings("ignore")
    # Set time period



    cdt_date = datetime.utcnow()
    cdt_yr = cdt_date.year
    cdt_mo = cdt_date.month
    cdt_day = cdt_date.day
    cdt_yrmoday = cdt_date.strftime('%Y%m%d')
    cdt_hour= cdt_date.hour

    if int(cdt_date.strftime("%H")) >= 4 and int(cdt_date.strftime("%H")) <= 11:
        init_time_hr = '00'
        start = cdt_date.replace(hour=0,minute=0,second=0,microsecond=0)
        end =cdt_date.replace(hour=0,minute=0,second=0,microsecond=0)
        start_3h = start + timedelta(hours=-3)
        end_3h = end + timedelta(hours=-3)
    elif int(cdt_date.strftime("%H")) >= 16 and int(cdt_date.strftime("%H")) <= 23:
        init_time_hr = '12'
        start = cdt_date.replace(hour=12)
        end = cdt_date.replace(hour=12)
        start_3h = start + timedelta(hours=-3)
        end_3h = end + timedelta(hours=-3)
    else:
        init_time_hr = '00'  # input('Enter the model run time ')
        start = cdt_date.replace(hour=0,minute=0,second=0,microsecond=0)
        end = cdt_date.replace(hour=0,minute=0,second=0,microsecond=0)
        start_3h = start + timedelta(hours=-3)
        end_3h = end + timedelta(hours=-3)
    #print(start)
    #timedif= str(abs(int(init_time_hr)-cdt_hour)).zfill(2)
    #print(timedif)
    airports = airportsdata.load()  # key is the ICAO identifier (the default) # To get Coordinates from ICAO Codes
    response=requests.get("https://tgftp.nws.noaa.gov/data/observations/metar/cycles/"+init_time_hr+"Z.TXT")#+timedif+"Z.TXT")
    data = pd.read_csv(dirorigin+'/ressources/Data/airport_europe.csv') #Dataframe with all Stations of europe

    # load data using Python JSON module
    with open(dirorigin+'/ressources/Data/lite.json', 'r') as f:
        icao_to_meteostat = json.loads(f.read())
    # Flatten data
    icao_to_meteostat  = pd.json_normalize(icao_to_meteostat)  # , record_path =['identifiers'], meta=["id"])
    icao_to_meteostat = icao_to_meteostat.rename(columns={"location.longitude": "longitude", "location.latitude": "latitude"})
    #print(icao_to_meteostat .head()["identifiers.icao"])
    #print(airports["EBAM"]['elevation'])#['ETIC'])
    datawwfont = pd.read_csv(dirorigin+'/ressources/Data/wwfont.csv')  # Fontframe
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
    visibility=[]
    visual_range=[]
    lon=[]
    lat=[]
    weatherfont=[]
    weathersymbol=[]
    weathercolour=[]
    cc=[]
    #obsa=Metar.Metar("ETIC 031755Z AUTO 29011KT 9999 -RA FEW008 BKN012 BKN019 OVC026 06/05 A3010 RMK AO2 CIG 010V019 SLP205 P0003 60009 T00570047 10057 20049 53017")
    #print(obsa.trend())
    for i in tqdm(range(len(splitting))):
        #if "ED" in splitting[i] != False:
        #if splitting[i].startswith('ED'):# or splitting[i].startswith('ET'):
        if any(splitting[i].startswith(ele) for ele in listofairports):
            #weather.append(splitting[i])
            try:
                obs = Metar.Metar(splitting[i])
                station.append(obs.station_id)
                time.append(obs.time)
                lon.append(airports[obs.station_id]['lon'])
                lat.append(airports[obs.station_id]['lat'])
                try:
                    cc.append(cloudcover(obs))
                except:
                    cc.append(None)
                try:
                    weather.append(metarww(obs.present_weather()))
                    weatherfont.append(datawwfont.iloc[metarww(obs.present_weather())]["font"])
                    weathersymbol.append(datawwfont.iloc[metarww(obs.present_weather())]["letter"])
                    weathercolour.append(datawwfont.iloc[metarww(obs.present_weather())]["colour"])
                except:
                    weather.append(None)
                    weatherfont.append(datawwfont.iloc[0]["font"])
                    weathersymbol.append(datawwfont.iloc[0]["letter"])
                    weathercolour.append(datawwfont.iloc[0]["colour"])

                try:
                    temperature.append(obs.temp.value())
                except AttributeError :
                    temperature.append(99999)
                try:
                    #print(obs.vis)
                    visibility.append(obs.vis.value())
                except AttributeError :
                    visibility.append(99999)

                try:
                    visual_range.append(obs.runway.value())
                except AttributeError :
                    visual_range.append(99999)


                try:
                    #sl_pressure.append(pressurereduction(obs.press.value(),airports[obs.station_id]["elevation"],obs.temp.value()))
                    sl_pressure.append(
                        calculate_sea_level_pressure(obs.press.value(), airports[obs.station_id]["elevation"], obs.temp.value()))

                except AttributeError :
                    sl_pressure.append(99999)


                try:
                    pressure.append(obs.press.value())
                except AttributeError :
                    pressure.append(99999)


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
               # print("The following Error occurred", err)
                pass

    ## Construct Dataframe
    d = {"station":station, "lat":lat,"lon":lon,"time":time,"weather":weather, "weatherfont":weatherfont,"weathersymbol":weathersymbol,"weathercolour":weathercolour,"temperature":temperature,"pressure":pressure,"sl_pressure":sl_pressure,"dewpoint":dewpoint, "windspeed":windspeed, "winddir":winddir, "visibility": visibility ,"visual_range":visual_range, "cloudcover":cc}

    df=pd.DataFrame(d)

    #metardata = df.loc[:, ~(df == '99999').any()]
    #print(df.tail())
    df=df.drop_duplicates(subset=['station'], keep="last") # Only use the latest Metar in that Timeframe
    #print(df.tail())

    # Supplement Missing Values via Meteostat Api
    listofairports =set(listofairports)
    listofairportsfound = df['station'].tolist()
    remainingairports = listofairports.difference(listofairportsfound)
    #print(listofairportsfound)
    print("Supplementing starting")
    pressure3h_change = []
    listofairportsfound_meteostat=[]
    for i in listofairportsfound:
        #icao_to_meteostat[icao_to_meteostat["identifiers.icao"] == i].id.squeeze()
        listofairportsfound_meteostat.append(icao_to_meteostat[icao_to_meteostat["identifiers.icao"] == i].id.squeeze())
    #listofairportsfound_meteostat = [i if isinstance(i, str) else 'None' for i in listofairportsfound_meteostat]
    listofairportsfound_meteostat = [i for i in listofairportsfound_meteostat if isinstance(i,str)]
    #print(listofairportsfound_meteostat)
    data_3h = Hourly(listofairportsfound_meteostat, start_3h, end_3h)
    data_3h = data_3h.fetch()
    rainer=[]
    #print(data_3h.head())
    print("Supplementing request finished")
    #metarcompare = duplicatedremove.to_csv(dirorigin+'/BUFR/metarcompare.csv', index = True)
    for i in tqdm(listofairportsfound):
        pressure_after= df[df["station"] == i ].pressure.squeeze()

        if isinstance(icao_to_meteostat[icao_to_meteostat["identifiers.icao"] == i].id.squeeze(),str):
            try:
                pressure_before= data_3h.loc[icao_to_meteostat[icao_to_meteostat["identifiers.icao"] == i].id.squeeze()].pres.squeeze()
            except:
                pressure_before = pressure_after
            try:
                rain= data_3h.loc[icao_to_meteostat[icao_to_meteostat["identifiers.icao"] == i].id.squeeze()].prcp.squeeze()
            except:
                rain=0
        else:
            pressure_before= pressure_after
            rain=0

        rainer.append(rain)
        diffpress= pressure_after -pressure_before
        pressure3h_change.append(diffpress)

    df = df.assign(pressure3h_change=pressure3h_change,rain=rainer)
    df=nclwwstring(df)
    metar_csv_data = df.to_csv(dirorigin+'/ressources/Data/metarsupp.csv', index = True)
    #metarcompare = duplicatedremove.to_csv(dirorigin+'/BUFR/metarsupp.csv', index = True)

    ## Dataframe for Groundlevel only

    remainingairportsmeteostat=[]
    for i in remainingairports:
        remainingairportsmeteostat.append(icao_to_meteostat[icao_to_meteostat["identifiers.icao"] == i].id.squeeze())
    remainingairportsmeteostat = [i for i in listofairportsfound_meteostat if isinstance(i,str)]

    data_remaining = Hourly(listofairportsfound_meteostat, start, end)
    data_remaining = data_remaining.fetch()
    #print(data_remaining.head())
    list_of_stations = df['station'].tolist()
    lon = df['lon'].tolist()
    lat = df['lat'].tolist()
    weatherfont = df['weatherfont'].tolist()
    weathersymbol = df['weathersymbol'].tolist()
    weathercolour = df['weathercolour'].tolist()
    for x in data_remaining.index:
        #print(x[0])
        try:
            list_of_stations.append(icao_to_meteostat[icao_to_meteostat["id"] == x[0]].id.squeeze())
        except:
            list_of_stations.append(None)
        try:
            lat.append(icao_to_meteostat[icao_to_meteostat["id"] == x[0]].latitude.squeeze())
        except:
            lat.append(lat)
        try:
            lon.append(icao_to_meteostat[icao_to_meteostat["id"] == x[0]].longitude.squeeze())
        except:
            lon.append(None)
        try:
            wwcode = datawwfont.index[datawwfont["Meteostat Code"] == int(data_remaining["coco"].loc[x[0]])][0]

        except ValueError:
            wwcode = 0

        # print(wwcode)
        try:
            weatherfont.append(datawwfont.iloc[wwcode]["font"])  # int(data["coco"].loc[x[0]])]["font"]

        except ValueError:
            weatherfont.append(None)

        try:
            weathersymbol.append(datawwfont.iloc[wwcode]["letter"])

        except ValueError:
            weathersymbol.append(None)

        try:
            weathercolour.append(datawwfont.iloc[wwcode]["colour"])

        except ValueError:
            weathercolour.append(None)

    # Transformations for  NCL
    #data = data.assign(lat=lat, lon=lon, weatherfont=weatherfont, weathersymbol=weathersymbol,                       weathercolour=weathercolour)

    datare = pd.DataFrame({'station': list_of_stations, 'lat': lat,'lon':lon, 'weatherfont':weatherfont, 'weathersymbol':weathersymbol,
                       'weathercolour':weathercolour})
    datare=nclwwstring(datare)
    metar_groundlevel = datare.to_csv(dirorigin+'/ressources/Data/metar_groundlevel.csv', index = True)

#def main():
 #  metarrequest("/home/alex/PycharmProjects/imuk")
#main()
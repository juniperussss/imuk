import xarray as xr
import pandas as pd
from datetime import datetime
import numpy as np


def requestmeteogram(model="icon", output_path= "products/meteogram/", time = datetime.now()):
    data_path = "database/input/"+model+  time.strftime("/%Y/")+time.strftime("%m").lstrip("0") +"/"+ time.strftime("%d").lstrip("0") + "/" +time.strftime("%H").zfill(2) +"/"   #"/2024/3/12/00/"
    print(data_path)
    date_string = time.strftime("%Y%m%d%H")#"2024031200"
    print(date_string)
    start_date = time #pd.to_datetime(date_string, format='%Y%m%d%H')
    lat_han = 52.5
    lon_han = 9.75

    variables = ["t2m", "prmsl", "t","tp","u10","v10","u","v","u","u","u","u","v","v","v","v","d2m","fg10","WW"]  # Liste der Variablen, die extrahiert werden sollen
    sub_variables = ["","", "/850","","","","/300","/300","/500","/700","/850","/950","/500","/700","/850","/950","","",""]
    folder_variables = ["t_2m", "pmsl","t","tot_prec","u_10m","v_10m","u","v","u","u","u","u","v","v","v","v","td_2m","vmax_10m","ww"]  # Liste der Variablen, die extrahiert werden sollen
    single_variables = ["", "_single-level","","","","","","","","","","","","","","","","","_single-level"]
    levels_variables = ["", "","_850","","","","_300","_300","_500","_700","_850","_950","_500","_700","_850","_950","","",""]
    single_variables_eu_d2 = ["_single-level", "_single-level","_pressure-level","_single-level","_single-level","_single-level","_pressure-level","_pressure-level","_pressure-level","_pressure-level"
    ,"_pressure-level","_pressure-level","_pressure-level","_pressure-level","_pressure-level","_pressure-level","_single-level","_single-level","_single-level"]
    # Leeres Dictionary für die Werte der Variablen
    variable_values = {f"{variable}{levels_variable}": [] for variable, levels_variable in zip(variables, levels_variables)}

    # Leere Liste für die Zeitstempel
    timestamps = []

    # Iteration durch jede Stunde


    if model == "icon":
        for hour in range(0, 181, 3):  # Von 0 bis 180 in 3-Stunden-Schritten
        # Iteration durch jede Variable
            for variable, folder_variable, single_variable, levels_variable, sub_variable, single_variables_eu_d2e in zip(variables, folder_variables, single_variables, levels_variables, sub_variables,single_variables_eu_d2):
                #print(variable)
           
                file_path = data_path + f"{folder_variable}{sub_variable}/ofile{single_variable}_{date_string}_{hour:03d}{levels_variable}_{folder_variable.upper()}.grib2"
                #print(file_path)
                try:
                    with xr.open_dataset(file_path, engine="cfgrib") as ds:
                        value = ds[variable].sel(longitude=lon_han, latitude=lat_han).values.item()
                        variable_values[f"{variable}{levels_variable}"].append(value)
                        #print(variable,value)
                except:

                    variable_values[f"{variable}{levels_variable}"].append(np.nan)
                    pass


            
        
        # Generiere den Zeitstempel für jede Stunde
            timestamp = start_date + pd.Timedelta(hours=hour)
            timestamps.append(timestamp)

        print(variable_values)
    
    elif model == "icon-eu":

        for hour in range(0, 120, 3):  # Von 0 bis 180 in 3-Stunden-Schritten
        # Iteration durch jede Variable
            for variable, folder_variable, single_variable, levels_variable, sub_variable, single_variables_eu_d2e in zip(variables, folder_variables, single_variables, levels_variables, sub_variables,single_variables_eu_d2):

                file_path = data_path + f"{folder_variable}{sub_variable}/icon-eu_europe_regular-lat-lon{single_variables_eu_d2e}_{date_string}_{hour:03d}{levels_variable}_{folder_variable.upper()}.grib2"
                try:

                    with xr.open_dataset(file_path, engine="cfgrib") as ds:
                        value = ds[variable].sel(longitude=lon_han, latitude=lat_han).values.item()
                        variable_values[f"{variable}{levels_variable}"].append(value)
                except:

                    variable_values[f"{variable}{levels_variable}"].append(np.nan)
                    pass
        
            # Generiere den Zeitstempel für jede Stunde
            timestamp = start_date + pd.Timedelta(hours=hour)
            timestamps.append(timestamp)
        print(variable_values)

    
    elif model == "icon-d2":

        for hour in range(0, 48, 3):  # Von 0 bis 180 in 3-Stunden-Schritten
        # Iteration durch jede Variable
            for variable, folder_variable, single_variable, levels_variable, sub_variable, single_variables_eu_d2e in zip(variables, folder_variables, single_variables, levels_variables, sub_variables,single_variables_eu_d2):
                if single_variables_eu_d2e == "_pressure-level":
                    file_path = data_path + f"{folder_variable}{sub_variable}/icon-d2_germany_regular-lat-lon{single_variables_eu_d2e}_{date_string}_{hour:03d}{levels_variable}_{folder_variable}.grib2"

                else:
                    file_path = data_path + f"{folder_variable}{sub_variable}/icon-d2_germany_regular-lat-lon{single_variables_eu_d2e}_{date_string}_{hour:03d}{levels_variable}_2d_{folder_variable}.grib2"
                try:
                    with xr.open_dataset(file_path, engine="cfgrib") as ds:
                        #print(ds)
                        value = ds[variable].sel(longitude=lon_han, latitude=lat_han, method="nearest").values.item()
                        variable_values[f"{variable}{levels_variable}"].append(value)
                except:
                    try:
                        with xr.open_dataset(file_path, engine="cfgrib",filter_by_keys={'stepUnits': 0}) as ds:
                            #print(ds)
                            value = ds[variable].sel(longitude=lon_han, latitude=lat_han, method="nearest").values.item()
                            variable_values[f"{variable}{levels_variable}"].append(value)
                    except:

                        variable_values[f"{variable}{levels_variable}"].append(np.nan)
                        pass

            
            # Generiere den Zeitstempel für jede Stunde
            timestamp = start_date + pd.Timedelta(hours=hour)
            timestamps.append(timestamp)
    
    else:
        print("Error Model not found ", model)



    # Konvertiere die Listen in Xarrays
    variable_xr = {variable: xr.DataArray(values, dims=['time'], coords={'time': timestamps}) for variable, values in variable_values.items()}

    # Kombiniere die Xarrays zu einem Dataset
    combined_ds = xr.Dataset(variable_xr)
       # Füge u und v als Variablen mit Geschwindigkeitsattributen hinzu
    combined_ds['u10'].attrs['units'] = 'm/s'
    combined_ds['v10'].attrs['units'] = 'm/s'

    print(combined_ds["WW"])
    combined_ds.to_netcdf(output_path +"meteogramm_"+model+".nc")
    return

requestmeteogram(model="icon",output_path="/mnt/nvmente/CODE/imuk/database/input/meteogram/",time =datetime(2024, 4, 23, 12, 0, 0))
requestmeteogram(model="icon-eu",output_path="/mnt/nvmente/CODE/imuk/database/input/meteogram/",time =datetime(2024, 4, 23, 12, 0, 0))
requestmeteogram(model="icon-d2",output_path="/mnt/nvmente/CODE/imuk/database/input/meteogram/",time =datetime(2024, 4, 23, 12, 0, 0))
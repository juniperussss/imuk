import xarray as xr
import pandas as pd


def requestmeteogram(model="icon"):
    data_path = "database/input/"+model+"/2024/3/12/00/"
    date_string = "2024031200"
    start_date = pd.to_datetime(date_string, format='%Y%m%d%H')
    lat_han = 52.5
    lon_han = 9.75

    variables = ["t2m", "prmsl", "t","tp","u10","v10","u","v"]  # Liste der Variablen, die extrahiert werden sollen
    sub_variables = ["","", "/850","","","","/300","/300"]
    folder_variables = ["t_2m", "pmsl","t","tot_prec","u_10m","v_10m","u","v"]  # Liste der Variablen, die extrahiert werden sollen
    single_variables = ["", "_single-level","","","","","",""]
    levels_variables = ["", "","_850","","","","_300","_300"]
    # Leeres Dictionary für die Werte der Variablen
    variable_values = {f"{variable}{levels_variable}": [] for variable, levels_variable in zip(variables, levels_variables)}

    # Leere Liste für die Zeitstempel
    timestamps = []

    # Iteration durch jede Stunde
    for hour in range(0, 181, 3):  # Von 0 bis 180 in 3-Stunden-Schritten
        # Iteration durch jede Variable
        for variable, folder_variable, single_variable, levels_variable, sub_variable in zip(variables, folder_variables, single_variables, levels_variables, sub_variables):
            file_path = data_path + f"{folder_variable}{sub_variable}/ofile{single_variable}_{date_string}_{hour:03d}{levels_variable}_{folder_variable.upper()}.grib2"
            with xr.open_dataset(file_path, engine="cfgrib") as ds:
                value = ds[variable].sel(longitude=lon_han, latitude=lat_han).values.item()
                variable_values[f"{variable}{levels_variable}"].append(value)
        
        # Generiere den Zeitstempel für jede Stunde
        timestamp = start_date + pd.Timedelta(hours=hour)
        timestamps.append(timestamp)

    # Konvertiere die Listen in Xarrays
    variable_xr = {variable: xr.DataArray(values, dims=['time'], coords={'time': timestamps}) for variable, values in variable_values.items()}

    # Kombiniere die Xarrays zu einem Dataset
    combined_ds = xr.Dataset(variable_xr)
       # Füge u und v als Variablen mit Geschwindigkeitsattributen hinzu
    combined_ds['u10'].attrs['units'] = 'm/s'
    combined_ds['v10'].attrs['units'] = 'm/s'

    print(combined_ds)
    combined_ds.to_netcdf("products/meteogram/meteogramm_"+model+".nc")
    return

requestmeteogram()

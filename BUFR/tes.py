from frost.client import APIError, Frost
f = Frost("d4a6401c-954e-4f95-89eb-b7828541f523") #Frost-Api-Key
res = f.get_sources(name='Hannover')

# return as Pandas Dataframe (requires Pandas installed)
df = res.to_df()

# return IDs of sources as list
ids = res.to_ids_list()
print(ids)


f = Frost("d4a6401c-954e-4f95-89eb-b7828541f523") #Frost-Api-Key
#res = f.get_available_timeseries(elements='weather_type')
res = f.get_available_timeseries(sources='SN1033800')

# return as Pandas Dataframe
df = res.to_df()

print(df.head())
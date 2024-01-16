from frost.client import APIError, Frost
f = Frost("d4a6401c-954e-4f95-89eb-b7828541f523") #Frost-Api-Key
res = f.get_observations(
            sources=['SN18700'],
            elements=['weather_type'],
            referencetime='2023-02-01/2023-02-02')
df = res.to_df()

print(df.head)

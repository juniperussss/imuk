import pandas as pd
#import csv
#file =open("../documentation/StationSearchResults.csv","r")

#data= list(csv.reader(file,delimiter=","))
#file.close()
d = pd.read_csv('../documentation/StationSearchResults.csv')
print(d.head())
print(d.loc[d['Latitude']==52.464428])
print(52.464428 in d.values)

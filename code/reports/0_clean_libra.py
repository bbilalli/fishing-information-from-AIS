import pandas as pd

file = pd.read_csv(r'./libra.csv')

# Select useful variables

file = file[['Marea (Descripción)','Barco Lote (Descripción)','Fecha','LAT','LONG','Temp','Sit.','KN','KB','ESPECIE (Descripción)','CORTE (Descripción)','TAMAÑO (Descripción)']]


# Select poteros
ceibe = file[file['Barco Lote (Descripción)']=='CEIBE DOUS']
luis = file[file['Barco Lote (Descripción)']=='DON LUIS I']
mateo = file[file['Barco Lote (Descripción)']=='SAN MATEO']
orion3 = file[file['Barco Lote (Descripción)']=='ORION 3']
francisco = file[file['Barco Lote (Descripción)']=='DON FRANCISCO I']
orion5 = file[file['Barco Lote (Descripción)']=='ORION 5']

data = ceibe.append([luis,mateo,orion3,orion5,francisco])

columns = ['Marea','Embarcacion','Day','Lat','Lon','Temperature','Sit.','KN','KB','Especie','Corte','Tamaño']
data.columns = columns

data['Day'] = pd.to_datetime(data['Day'], format="%d/%m/%y")
data['Day'] = data['Day'].dt.strftime('%Y-%m-%d 00:00:00')
data['KN'] = data['KN'].str.replace(",", "")
data['KN'] = pd.to_numeric(data['KN'])
data['KB'] = data['KB'].str.replace(",", "")
data['KB'] = pd.to_numeric(data['KB'])

data['Marea'] = data['Marea'].str.replace(" ", "").str.split('-').str.get(1).str.replace('EA','EA ')

data['Temperature'] = data['Temperature'].str.replace(",", ".")
data['Temperature'] = data['Temperature'].str.replace("°", " ")
data['Temperature'] = data['Temperature'].str.split().str.get(0)
data['Temperature'] = pd.to_numeric(data['Temperature'])

data['Lat'] = data['Lat'].str.replace("'", "")
data['Lat'] = data['Lat'].str.replace("º", " ")
data['Lat'] = data['Lat'].str.replace("S/C", "")


data['LatG'] = data['Lat'].str.split().str.get(0).apply(float)
data['LatM'] = data['Lat'].str.split().str.get(1).apply(float)

data['Lat'] = data['LatG']+data['LatM']/60

data['Lon'] = data['Lon'].str.replace("'", "")
data['Lon'] = data['Lon'].str.replace("º", " ")

data['LonG'] = data['Lon'].str.split().str.get(0).apply(float)
data['LonM'] = data['Lon'].str.split().str.get(1).apply(float)

data['Lon'] = data['LonG']+data['LonM']/60


data = data.drop(columns=['LatG','LatM','LonG','LonM'])
columns = ['Marea','Embarcacion','Day','Latitude','Longitude','Temperature','Sit.','KN','KB','Especie','Corte','Tamaño']
data.columns = columns

data.to_csv('libra_clean.csv',index=False)

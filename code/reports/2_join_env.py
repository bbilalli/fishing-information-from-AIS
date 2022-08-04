import pandas as pd

kg = pd.read_csv(r'./kg.csv')
lines = pd.read_csv(r'./lines.csv')

# DURATION: MINUMUM ONE HOUR
kg = kg[kg['Duration']!=0]
kg['Duration'] = [1 if x<1 else x for x in kg['Duration']]

# NORMALIZE KG
kg = pd.merge(kg,lines)
kg['NKg'] = kg['Kg']/kg['Lineas']
kg['NHKg'] = kg['NKg']/kg['Duration']

# PAPAECOS
papa = pd.read_csv(r'./papaecos.csv')

kg = pd.merge(kg,papa)

# ENVIROMENTAL

env = pd.read_csv(r'./environmental.csv')

kg = pd.merge(kg,env)

# PREPROCESS DATA

kg = kg.rename(columns={'TempOrigin': 'ImputedTemp', 'ChlorOrigin': 'ImputedChlor'})
kg['NoCloudTemp'] = [True if x=='Actual' else False for x in kg['ImputedTemp']]
kg['NoCloudChlor'] = [True if x=='Actual' else False for x in kg['ImputedChlor']]
kg['NoCloud'] = kg['NoCloudChlor']*kg['NoCloudTemp']

kg['ImputedTemp'] = [False if x=='Actual' else True for x in kg['ImputedTemp']]
kg['ImputedChlor'] = [False if x=='Actual' else True for x in kg['ImputedChlor']]

kg['Year'] = kg['Day'].str[0:4]
kg['Month'] = kg['Day'].str[5:7]


kg = kg[['Embarcacion','Day','Year','Month','Kg','NKg','NHKg','Light','Phase','Temperature','Chlorophyll','Wind','SLA','Elevation','Duration','NoCloud','Lineas','Latitude','Longitude','PapaEcho','Quadrant','ImputedTemp','ImputedChlor']]




kg.to_csv(r'integrated.csv',index=False)


import pandas as pd
from datetime import timedelta
import numpy as np
from geopy import distance


cross_hard = False
data = pd.read_csv(r'./ais.csv')


#ADD TO EXTRA COLUMNS:
# - DURATION TILL NEXT TIMESTAMP
# - ARE BOTH TIMESTAMPS ARE GOING IN AN ACCEPTABLE VELOCITY AND ARE INSIDE THE FISHING PERIOD? T/F

threshold = 1.5  #mph
start = 10 #start of no fishing period
end = 16 #end of no fishing period
radius = 100 #fishing zone outside harbours

data['Fecha'] = pd.to_datetime(data['Fecha']) #CONVERT DATA TO DATETIME FORMAT

data['Duration'] = (data['Fecha'].shift(-1)-data['Fecha']).dt.seconds/60
data['Fishing'] = ((data['Velocidad']<threshold) & (data['Velocidad'].shift(-1)<threshold))*[False if (x.hour+x.minute/60)>start and (x.hour+x.minute/60)<end else True for x  in data['Fecha']]


# WE ASSUME THAT THEY ISSUE THE FISHING REPORT AT THE END, SO THE DAY IN THE PESCA_POTEROS DATASET IS AT THE END OF
# THE FISHING DAY. HENCE, FOR INSTANCE FOR THE DAY 2020-01-12 THE FISHING PERIOD WILL GO FROM 12:00 OF 2020-01-11
# TO 12:00 OF 2020-01-12. WE WILL ADD A NEW COLUMN FOR THE 'ARBITRARY' DAY THEY ARE AT:

data['Day'] = [x if (x.hour+x.minute/60)<12 else x+timedelta(days=1) for x  in data['Fecha']]
data['Day'] = data['Day'].dt.strftime('%Y-%m-%d 00:00:00')

# TRANSFORM POSITION TO GRID

data['GridLat'] = [np.ceil(x)-0.25 if abs(x-np.ceil(x))<0.5 else np.ceil(x)-0.75 for x in data['Latitud']]
data['GridLon'] = [np.ceil(x)-0.25 if abs(x-np.ceil(x))<0.5 else np.ceil(x)-0.75 for x in data['Longitud']]

# REMOVE ROWS WHERE THEY ARE NOT FISHING
data = data[data['Fishing']==True]

# REMOVE ROWS WHERE THEY ARE AT HARBOUR
data = data[((data['Latitud']!=data['Latitud'].shift(-1)) & (data['Longitud']!=data['Longitud'].shift(-1))) & ((data['Latitud']!=data['Latitud'].shift(1)) & (data['Longitud']!=data['Longitud'].shift(1)))]

if cross_hard:
    harb = pd.read_csv(r'./harbours.csv')
    km = []
    for i in range(len(data)):
        min = radius+60
        for j in range(len(harb)):
            dd = distance.distance((data.iloc[i,2],data.iloc[i,3]),(harb.iloc[j,0],harb.iloc[j,1])).km
            if dd<radius:
                min = dd
        
        km.append(min)

    data['km']=km

    data = data[data['km']>=(radius+60)]
    

data.to_csv(r'./ais_fishing.csv',index=False)

# REMOVE UNWANTED COLUMNS
data = data[['Embarcacion','Day','Duration','GridLat','GridLon']]

# WE SUM DE DURATION GROUPED BY BOAT,DAY AND GRID QUADRANT

duration = data.groupby(['Embarcacion', 'Day','GridLat','GridLon']).sum().reset_index() 
duration['Duration'] = duration['Duration']/60

# WE SUM AS WELL FOR THE TOTAL OF THE DAY, IN ORDER TO COMPUTE THE FRACTION IN EACH QUADRANT
data = data[['Embarcacion','Day','Duration']]
total_duration = data.groupby(['Embarcacion', 'Day']).sum().reset_index() 
total_duration['Duration'] = total_duration['Duration']/60
total_duration.rename(columns={"Duration": "Total_Duration"},inplace=True)

# MERGE THE TWO DURATION DATASETS
duration = pd.merge(duration,total_duration)
duration['Frac'] = duration['Duration']/duration['Total_Duration']
duration = duration.drop(columns=['Total_Duration'])
# SAVE CSV
duration.to_csv(r'./fishing_quadrants.csv',index=False)


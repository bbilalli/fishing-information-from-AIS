import pandas as pd
from datetime import timedelta
import numpy as np
from geopy import distance



data = pd.read_csv(r'./ais.csv')


#ADD TO EXTRA COLUMNS:
# - DURATION TILL NEXT TIMESTAMP
# - ARE BOTH TIMESTAMPS ARE GOING IN AN ACCEPTABLE VELOCITY AND ARE INSIDE THE FISHING PERIOD? T/F

threshold = 1.5  #mph
start = 10 #start of no fishing period
end = 16 #end of no fishing period
duration = True #filter by duration
min_hours = 1 #minimum of hours to be considered fishing
cross_harb = True #remove close proimity to harbour
radius = 100 #distance to port

data['Fecha'] = pd.to_datetime(data['Fecha']) #CONVERT DATA TO DATETIME FORMAT

data['Duration'] = (data['Fecha'].shift(-1)-data['Fecha']).dt.seconds/60
data['Fishing'] = ((data['Velocidad']<threshold) & (data['Velocidad'].shift(-1)<threshold))*[False if (x.hour+x.minute/60)>start and (x.hour+x.minute/60)<end else True for x  in data['Fecha']]


# WE ASSUME THAT THEY ISSUE THE FISHING REPORT AT THE END, SO THE DAY IN THE PESCA_POTEROS DATASET IS AT THE END OF
# THE FISHING DAY. HENCE, FOR INSTANCE FOR THE DAY 2020-01-12 THE FISHING PERIOD WILL GO FROM 12:00 OF 2020-01-11
# TO 12:00 OF 2020-01-12. WE WILL ADD A NEW COLUMN FOR THE 'ARBITRARY' DAY THEY ARE AT:

data['Day'] = [x if (x.hour+x.minute/60)<12 else x+timedelta(days=1) for x  in data['Fecha']] #Tomorrow
#data['Day'] = [x-timedelta(days=1) if (x.hour+x.minute/60)<12 else x for x  in data['Fecha']] #Yesterday
data['Day'] = data['Day'].dt.strftime('%Y-%m-%d 00:00:00')
#data['Day'] = data['Fecha'].dt.strftime('%Y-%m-%d 00:00:00')

# TRANSFORM POSITION TO GRID

data['GridLat'] = [np.ceil(x)-0.25 if abs(x-np.ceil(x))<0.5 else np.ceil(x)-0.75 for x in data['Latitud']]
data['GridLon'] = [np.ceil(x)-0.25 if abs(x-np.ceil(x))<0.5 else np.ceil(x)-0.75 for x in data['Longitud']]

# REMOVE ROWS WHERE THEY ARE NOT FISHING
data = data[data['Fishing']==True]



# REMOVE ROWS WHERE THEY ARE AT HARBOUR, FIRST BASED ON LONG PERIODS OF TIME STATIC
data = data[((data['Latitud']!=data['Latitud'].shift(-1)) & (data['Longitud']!=data['Longitud'].shift(-1))) & ((data['Latitud']!=data['Latitud'].shift(1)) & (data['Longitud']!=data['Longitud'].shift(1)))]

# REMOVE ZONES WITH LOW DURATION

if duration:
    data = data.groupby(['Embarcacion', 'Day','GridLat','GridLon']).sum().reset_index() 
    data['Duration'] = data['Duration']/60

    data = data[data['Duration']>=min_hours]


# REMOVE IF THEY ARE IN CLOSE PROXIMITY OF HARBOUR
data = data[['Embarcacion','Day','GridLat','GridLon']].drop_duplicates()

if cross_harb:
    harb = pd.read_csv(r'./harbours.csv')
    km = []
    for i in range(len(data)):
        print(i)
        min = radius+60
        for j in range(len(harb)):
            dd = distance.distance((data.iloc[i,2],data.iloc[i,3]),(harb.iloc[j,0],harb.iloc[j,1])).km
            if dd<radius:
                min = dd
        
        km.append(min)

    data['km']=km

    data = data[data['km']>=(radius+60)]



data = data[['Embarcacion','Day']].drop_duplicates()

data.to_csv(r'./fishing_ais.csv',index=False)



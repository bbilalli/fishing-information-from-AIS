import pandas as pd

import pandas as pd
from datetime import timedelta
import numpy as np
from pyparsing import col
from geopy import distance

data = pd.read_csv(r'./ais.csv')
end = pd.read_csv(r'./to_port.csv')

data['Fecha'] = pd.to_datetime(data['Fecha']) #CONVERT DATA TO DATETIME FORMAT
data['Day'] = data['Fecha'].dt.strftime('%Y-%m-%d 00:00:00')

#ADD EXTRA COLUMN:
# - ARE BOTH TIMESTAMPS ARE GOING IN AN ACCEPTABLE VELOCITY?

threshold = 1.5  #mph
data['Fishing'] = ((data['Velocidad']<threshold) & (data['Velocidad'].shift(-1)<threshold))

# TRANSFORM POSITION TO GRID
data['GridLat'] = [np.ceil(x)-0.25 if abs(x-np.ceil(x))<0.5 else np.ceil(x)-0.75 for x in data['Latitud']]
data['GridLon'] = [np.ceil(x)-0.25 if abs(x-np.ceil(x))<0.5 else np.ceil(x)-0.75 for x in data['Longitud']]


# REMOVE UNWANTED VARIABLES
data = data.drop(columns=['Fecha','Latitud','Longitud','Curso','Velocidad'])

# WE GET FOR EACH DAY, IN WHICH QUADRANTS WE DID FISH AND AS WELL IN WHICH WE DID NOT FISH. THEY MIGHT NOT BE DISJOINT
fish = data[data['Fishing']==True].groupby(['Embarcacion', 'Day','GridLat','GridLon']).sum().reset_index()
no_fish = data[data['Fishing']==False].groupby(['Embarcacion', 'Day','GridLat','GridLon']).sum().reset_index()
fish = fish.drop(columns=['Fishing'])
no_fish = no_fish.drop(columns=['Fishing'])

# WE GET THE QUADRANT IS WHICH THEY BOTH FISHED AND NOT FISHED IN THE SAME DAY --> FISHED
joint = pd.merge(no_fish,fish)

# DISJOINT NO FISH
disjoint = pd.concat([no_fish,joint]).drop_duplicates(keep=False)


# WE REMOVE THE DAY IN WHICH THEY RETURN 

end = pd.merge(disjoint,end)
disjoint = pd.concat([disjoint,end]).drop_duplicates(keep=False)



# REMOVE EMBARCACION

ais = disjoint.drop(columns=['Embarcacion'])
ais = ais.drop_duplicates(keep='first')

# REMOVE LOCATIONS ABOVE PARALLEL 44 IN VEDA TIMES
ais['Day'] = pd.to_datetime(ais.Day)
bad = ais[(ais['Day'].dt.month.astype(int)<4) & (ais['GridLat']>-44)]

ais = pd.concat([ais,bad]).drop_duplicates(keep=False)

# REMOVE CLOSE LOCATIONS
ports = pd.read_csv(r'./harbours.csv')


km = []
for i in range(len(ais)):
    min = 160
    for j in range(len(ports)):
        dd = distance.distance((ais.iloc[i,1],ais.iloc[i,2]),(ports.iloc[j,0],ports.iloc[j,1])).km
        if dd<100:
            min = dd
    
    km.append(min)

ais['km']=km

ais = ais[ais['km']>=160]

ais['km'] = False

ais.columns = ['Day','Latitude','Longitude','Tag']

ais.to_csv(r'./no_fishing.csv',index=False)







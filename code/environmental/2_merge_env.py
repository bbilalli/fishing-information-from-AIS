from operator import index
import pandas as pd

moon = pd.read_csv(r'./moon.csv')
temp = pd.read_csv(r'./temp.csv')
chlor = pd.read_csv(r'./chlor.csv')
lag = pd.read_csv(r'./lag.csv')
bath = pd.read_csv(r'./bathymetry.csv')
wind = pd.read_csv(r'./wind.csv')
sla = pd.read_csv(r'./sla.csv')

lag = lag[['Day','Latitude','Longitude','11W']]


all = pd.merge(moon,temp,how='left')
all = pd.merge(all,chlor,how='left')
all = pd.merge(all,wind,how='left')
all = pd.merge(all,sla,how='left')
all = pd.merge(all,bath,how='left')
all = pd.merge(all,lag,how='left')

all.to_csv(r'./environmental.csv',index=False)
import pandas as pd

data = pd.read_csv(r'./libra_clean.csv')
data = data[['Embarcacion','Day','KN']]
data = data.groupby(['Embarcacion', 'Day']).sum().reset_index() 
data['Day'] = pd.to_datetime(data['Day'])
data['Day'] = data['Day'].dt.strftime('%Y-%m-%d 00:00:00')
data = data.sort_values(by=['Embarcacion', 'Day'])

quadrant = pd.read_csv(r'./fishing_quadrants.csv')
data = pd.merge(data,quadrant)
data['KN'] = data['KN']*data['Frac']
data = data.drop(columns=['Frac'])
data = data[data['KN']!=0]

data.to_csv(r'./kg.csv',index=False)



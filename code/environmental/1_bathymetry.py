import netCDF4 as nc4
import numpy as np
import pandas as pd
import csv



############# COORDINATES OF THE WANTED POINTS #####################

coords = pd.read_csv(r'.\coordinates.csv')
points_lat = coords['Latitud'].to_numpy()
points_lon =  coords['Longitud'].to_numpy()
points = []
for i,j in zip(points_lat,points_lon):
    points.append([i,j])


df = nc4.Dataset(r'\BATH\bath05.nc')


grid = 0.5

index = []
for point in points:
    latitude = point[0]
    longitude = point[1]
    ilat = int(abs(np.floor((90-latitude)/grid)))
    ilon = int(abs((-180-longitude)/grid))
    index.append([ilat,ilon])

with open(r'.\bathymetry.csv', 'a', newline="", encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(['Latitude','Longitude','Elevation'])
    for pos,point in zip(index,points):
        writer.writerow([point[0],point[1],df['elevation'][pos[0],pos[1]]])
# OS CHANGE
library(raster)
library(ncdf4)

r1 = raster('reference.nc') # Reference .nc file at 0.5x0.5 grid

path = '/TEMPERATURE/ALL'

file_list <- list.files(path=path)

## RESCALE TEMPERATURE AND WINF

for (value in file_list) {
  p = paste(path,'/',value,sep='')
  r2 = raster(p)
  names(r2) = 'sea_surface_temperature'
  r3 = resample(r2,r1)
  writeRaster(r3, paste('/TEMPERATURE/0.5/',value,sep=''))

  p = paste(path,'/',value,sep='')
  r2 = raster(p,varname ='wind_speed')
  names(r2) = 'wind_speed'
  r3 = resample(r2,r1)
  writeRaster(r3, paste('/WIND/0.5/',value,sep=''))
  } 

} 

## REESCALE CHLOROPHYLL

path = '/CHLOR/ALL'

file_list <- list.files(path=path)


for (value in file_list) {
  p = paste(path,'/',value,sep='')
  r2 = raster(p,varname='chlor_a')
  names(r2) = 'chlor_a'
  r3 = resample(r2,r1)
  writeRaster(r3, paste('/CHLOR/0.5/',value,sep=''))
} 

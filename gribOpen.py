import numpy as np
import pandas as pd
import pygrib
from collections import namedtuple

def closest_grid_point(in_lat, in_lon, grid=0.75):
    """Returns index of point closest to input"""
    out_lat = round(in_lat / grid, 0) * grid
    lat_idx = int((90 - out_lat) / 0.75)
    out_lon = round(in_lon / grid, 0) * grid + 180
    lon_idx = int(out_lon / 0.75)
    return (lat_idx, lon_idx)


grbs = pygrib.open('/home/tpk/testTemp.grib')
txt_stations = pd.read_csv('/home/tpk/hydro/stations.txt', header=None, 
                               delimiter=';')

Station = namedtuple('station', ['lat', 'lon', 'lat_idx', 'lon_idx'])

dct_station_info = {}
dct_station_data = {}
tcols = ['datetime','temp']
pcols = ['datetime','precip']

for index, row in txt_stations.iterrows():
    lat = row[1]
    lon = row[2]
    lat_idx, lon_idx = closest_grid_point(lat, lon)
    dct_station_info[row[0]] = Station(lat, lon, lat_idx, lon_idx)
    dct_station_data[row[0]+'_T'] = pd.DataFrame(columns=tcols)
    #dct_station_data[row[0]+'_P'] = pd.DataFrame(columns=pcols)


for grb in grbs[:2]:
    #print(grb.analDate)
    #print(grb.validDate)
    if grb['name'] == "2 metre temperature":
        for station in dct_station_info.keys():
            date_time = grb.analDate
            temperature = grb.values[dct_station_info[station].lat_idx, 
                                     dct_station_info[station].lon_idx]
            tmp_df = pd.DataFrame([[date_time, temperature]], columns=tcols)
            print(tmp_df)            
            dct_station_data[station+'_T'] = \
                            dct_station_data[station+'_T'].append(tmp_df)

#grb = grbs[1]
#print(grb.keys())

#print(grb['cfName'])
#print(grb['shortName'])
#print(grb['stepType'])
#print(grb['stepRange'])
#print(grb['startStep'])
#print(grb['endStep'])

    
#grbs.tell()
#grbs.seek(0)
#grbs.tell()
#tmp = grbs.select(name='2 metre temperature')
#count(tmp)
#data, lats, lons = grb1.data(lat1=38,lat2=46,lon1=13,lon2=32)
#data.shape, lats.min(), lats.max(), lons.min(), lons.max()





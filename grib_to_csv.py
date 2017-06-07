#!/usr/bin/env python
import pandas as pd
import pygrib
from collections import namedtuple
from datetime import datetime, timedelta

def closest_grid_point(in_lat, in_lon, grid=0.75):
    """Returns index of point closest to input"""
    out_lat = round(in_lat / grid, 0) * grid
    lat_idx = int((90 - out_lat) / 0.75)
    out_lon = round(in_lon / grid, 0) * grid + 180
    lon_idx = int(out_lon / 0.75)
    return (lat_idx, lon_idx)

stations_path = "/home/tpk/projects/ecmwf/stations.txt"
txt_stations = pd.read_csv(stations_path, header=None, delimiter=';')

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
    dct_station_data[row[0]+'_P'] = pd.DataFrame(columns=pcols)


path_root = "/home/tpk/projects/ecmwf/"
for wvar in ['temperature', 'precipitation']:
    for year in range(1991, 2017):
        start = str(year) + "-01-01"
        end = str(year) + "-12-31"
        grib_path = path_root + wvar + "_" + start + "_" + end + ".grib"
        grbs = pygrib.open(grib_path)
        print('Processing: ' + grib_path)
        for grb in grbs:
            date_time = grb.analDate + timedelta(hours=grb.endStep)
            for station in dct_station_info.keys():
                value = grb.values[dct_station_info[station].lat_idx, 
                                   dct_station_info[station].lon_idx]
                if grb.name == "2 metre temperature":
                    tmp_df = pd.DataFrame([[date_time, value]], columns=tcols)        
                    dct_station_data[station+'_T'] = \
                                        dct_station_data[station+'_T'].append(tmp_df)
                elif grb.name == "Total precipitation":
                    tmp_df = pd.DataFrame([[date_time, value]], columns=pcols)        
                    dct_station_data[station+'_P'] = \
                                        dct_station_data[station+'_P'].append(tmp_df)


save_path = "/home/tpk/projects/ecmwf/csv/"
for station in dct_station_data.keys():
    dct_station_data[station].to_csv(save_path + station + ".csv", sep=';', 
                                     index=False)
  
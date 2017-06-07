#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer

def download_grib(weather_var, start_date, end_date):
    '''
    weather_var: temperature or precipitation
    start_date, end_date: as string in format YYYY-MM-DD
    '''
    from_to_str = start_date + "/to/" + end_date
    save_str = "_" + start_date + "_" + end_date
    server = ECMWFDataServer()
    if weather_var == "temperature":
        server.retrieve({
            "class": "ei",
            "dataset": "interim",
            "date": from_to_str,
            "expver": "1",
            "grid": "0.75/0.75",
            "levtype": "sfc",
            "param": "167.128",
            "step": "0",
            "stream": "oper",
            "time": "00:00:00/06:00:00/12:00:00/18:00:00",
            "type": "an",
            "target": "/home/tpk/hydro/ecmwf/temperature" + save_str + ".grib",
        })
    elif weather_var == "precipitation":
        server.retrieve({
            "class": "ei",
            "dataset": "interim",
            "date": from_to_str,
            "expver": "1",
            "grid": "0.75/0.75",
            "levtype": "sfc",
            "param": "228.128",
            "step": "3/6/9/12",
            "stream": "oper",
            "time": "00:00:00/12:00:00",
            "type": "fc",
            "target": "/home/tpk/hydro/ecmwf/precipitation" + save_str + ".grib",
        })


if __name__ == "__main__":
    for year in range(1992, 2017):
        start = str(year) + "-01-01"
        end = str(year) + "-12-31"
        download_grib("precipitation", start, end)
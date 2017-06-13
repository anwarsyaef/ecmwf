import pandas as pd
from datetime import datetime, timedelta

save_path = "/home/tpk/projects/ecmwf/csv/"
temp_path = "/home/tpk/projects/ecmwf/csv/ARAD_T.csv"


data = pd.read_csv(temp_path, delimiter=';')



data['datetime'] = pd.to_datetime(data['datetime'], format='%Y-%m-%d %H:%M:%S')
data['datetime'][0].type

# data.insert(1, dftest['datetime'].
#df.insert(idx, col_name, value)

    

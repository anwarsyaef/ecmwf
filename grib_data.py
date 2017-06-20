import pandas as pd

stations_path = "/home/tpk/projects/ecmwf/stations.txt"
in_path = "/home/tpk/projects/ecmwf/csv/"
out_path = "/home/tpk/projects/ecmwf/csv/daily/"

K = 273.15

txt_stations = pd.read_csv(stations_path, header=None, delimiter=';')

for suffix in ['_T','_P']:
    for index, row in txt_stations.iterrows():
        name = row[0]
        path = in_path + name + suffix + '.csv'
        data = pd.read_csv(path, delimiter=';')
        data['datetime'] = pd.to_datetime(data['datetime'], format='%Y-%m-%d %H:%M:%S')        
        if suffix == '_P':
            data['datetime'] = data['datetime'] + pd.DateOffset(hours=-1)
            data.insert(1,'date',data['datetime'].dt.date)
            data.insert(2,'hour',data['datetime'].dt.hour)
            # df.loc[df['column_name'] == some_value]
            data = data.loc[data['hour'].isin([11,23])]
            daily = data.groupby('date').sum()
            daily = daily['precip'] * 1000
        else:
            data.insert(1,'date',data['datetime'].dt.date)
            # daily = data.groupby('date').mean()
            daily = data.groupby('date').min()
            daily = daily['temp'] - K
        daily.to_csv(out_path + name + suffix + ".csv", sep=';')
        print(name + suffix, ' daily data saved')



#data = pd.read_csv("/home/tpk/projects/ecmwf/csv/CELJE_P.csv", delimiter=';')
#data['datetime'] = pd.to_datetime(data['datetime'], format='%Y-%m-%d %H:%M:%S')        
#import matplotlib.pyplot as plt    
#import numpy as np
#dp = data['precip'].loc[:47]
#fig, ax = plt.subplots()
#ax.plot(dp)
#ax.set_xticks(np.arange(-1, 47, 4))
#ax.xaxis.grid(True, which='major')
#plt.show()
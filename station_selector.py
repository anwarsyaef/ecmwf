#!/usr/bin/env python3
import csv

#st_names = ['Austria','Germany','Slovenia','Croatia','Hungary',
#            'Bosnia and Herzegovina','Serbia','Romania','Montenegro']
st_names = ['Slovenia']
output = []

with open('EuropeWMO.csv', newline='') as csvfile:
    rawdata = csv.reader(csvfile, delimiter=';')
    for row in rawdata:
        if row[1] in st_names:
            #print(row[2], row[3], row[4])
            if row[3] != 'null':
                if float(row[3]) < 50 and float(row[3]) > 40:
                    if float(row[4]) > 8 and float(row[4]) < 30:                
                        outstr = (row[2].replace('/','_').replace('.','_'), row[3], row[4])
                        output.append(outstr)

with open('stations.txt', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerows(output)
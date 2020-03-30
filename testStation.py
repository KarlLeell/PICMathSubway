#==========================================
# Title:  Test Station Class
# Author: NYUPICMathSubwayGroup
# Date:   2020.02.24
# Comment:Need pandas to run this test

import pandas as pd
import argparse
from station import Station

def main(args):
  print(args.file_loc)
  sheet = station_file = pd.read_excel(args.file_loc)
  rows = len(sheet)
  stations = []
    for i in range(0, rows):
      # the location in file is actually the entry i think
      name = sheet.values[i, 8]
      boro = sheet.values[i, 6]
      routes = str(sheet.values[i, 7]).split(",")
      station = Station(name = name, boro = boro, routes = routes)    
      stations.append(station)              
 
    for n in range(0,len(stations)):
      stations[n].print()
      print()

    print('Number of stations:',len(stations))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('file_loc', type = str, default = 'NYCT FE Required Data/List of Stations and FCAs.xlsx')
  args = parser.parse_args()
  main(args)

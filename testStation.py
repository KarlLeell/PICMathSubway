#==========================================
# Title:  Test Station Class
# Author: NYUPICMathSubwayGroup
# Date:   2020.02.24
# Comment:Need pandas to run this test
#==========================================

import pandas as pd
import argparse
from station import Station

def main(args):
  print(args.file_loc)
  sheet = station_file = pd.read_excel(args.file_loc)
  rows = len(sheet)
  stations = []
  for i in range(1, rows):
    # the location in file is actually the entry i think
    name = sheet.values[i, 4]
    boro = sheet.values[i, 5]
    routes_str = sheet.values[i, 6]
    routes = [routes_str[i] for i in range(len(routes_str))]
    station = Station(name = name, boro = boro, routes = routes)
    stations.append(station)
  print(len(stations))
  stations[0].print()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('file_loc', type = str, default = 'NYCT FE Required Data/List of Stations and FCAs.xlsx')
  args = parser.parse_args()
  main(args)

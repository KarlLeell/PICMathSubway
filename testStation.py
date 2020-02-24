#==========================================
# Title:  Test Station Class
# Author: NYUPICMathSubwayGroup
# Date:   2020.02.24
# Comment:Need xlrd to run this test
#==========================================

import xlrd
import argparse
from Station import Station

def main(args):
  station_file = xlrd.open_workbook(args.file_loc)
  sheet = station_file.sheet_by_index(0) 
  rows = sheet.nrows
  stations = []
  for i in range(1, rows):
    # the location in file is actually the entry i think
    name = sheet.cell_value(i, 4)
    boro = sheet.cell_value(i, 5)
    routes_str = sheet.cell_value(i, 6)
    routes = [routes_str[i] for i in range(len(routes_str))]
    station = Station(name = name, boro = boro, routes = routes)
    stations.append(station)
  print(len(stations))
  stations[0].print()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('file_loc', type = str, default = 'NYCT FE Required Data/List of Stations and FCAs')
  args = parser.parse_args()
  main(args)

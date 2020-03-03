#==========================================
# Title:  Test Station Class
# Author: NYUPICMathSubwayGroup
# Date:   2020.03.02
# Comment:Need pandas to run this test
#==========================================

import numpy as np
import pandas as pd
import argparse
from station import Station
from gate import Gate
from subway_graph import Graph
import constants


def main(args):
  print(args.file_loc)
  sheet = pd.read_excel(args.file_loc)
  station_loc = pd.read_csv(args.station_loc)
  rows = len(sheet)
  wkd_graph = Graph(constants.DAY[0])
  sat_graph = Graph(constants.DAY[1])
  sun_graph = Graph(constants.DAY[2])
  #location for stations
  location_book = {}
  # build a map for stations and locations
  for i in range(len(station_loc)):
    station = station_loc.loc[i, 'Stop Name']
    latitude = station_loc.loc[i, 'GTFS Latitude']
    longitude = station_loc.loc[i, 'GTFS Longitude']
    location_book[station] = [latitude, longitude]



  for i in range(0, rows):
    gate_id = sheet.values[i, 1]
    day = sheet.values[i, 2]
    # begin_time has 24-hour format in form x00 where it actually means x:00
    # mod 24 because there are some 2400 to 2500 tasks
    begin_time = int(int(sheet.values[i, 3]) / 100 % 24)
    boro = sheet.values[i, 6]
    routes_str = str(sheet.values[i, 7])
    name = str(sheet.values[i, 8])
    routes = routes_str.split(',')
    task_matrix = np.zeros((24*12, 1))
    begin_entry = 12 * begin_time
    comments = sheet.values[i, 10]
    # mark the matrix
    for i in range(begin_entry, begin_entry+12):
      task_matrix[i, 0] = 1
    # get location of a station
    loc = location_book.get(name)
    if not loc:
      loc = []

    task = Gate(name = name, boro = boro, loc = loc, routes = routes, gate_id = gate_id, begin_time = begin_time,
                task_matrix = task_matrix, day = day, comments = comments)

    # adding vertex to graph
    if task.day == constants.DAY[0]:
      wkd_graph.add_vertex(task)
    elif task.day == constants.DAY[1]:
      sat_graph.add_vertex(task)
    elif task.day == constants.DAY[2]:
      sun_graph.add_vertex(task)

  #print and see the graphs
  wkd_graph.print()
  sat_graph.print()
  sun_graph.print()
  #wkd_graph.vertices[0][1].print()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--file_loc', default='NYCT FE Required Data/SFE SAMPLE210.xlsx', type=str)
  parser.add_argument('-s', '--station_loc', default='NYCT FE Required Data/station_location.csv', type=str)
  args = parser.parse_args()
  main(args)
  

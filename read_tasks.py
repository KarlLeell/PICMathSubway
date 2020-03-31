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
from tqdm import tqdm
import constants


def read(path):
  print('Reading tasks: '+ path[0])
  print('Station locations reference: '+ path[1])
  print('Station loc id reference: '+ path[2])
  print('Checker list: '+ path[3])
  sheet = pd.read_excel(path[0])
  station_loc = pd.read_csv(path[1])
  station_ls = pd.read_excel(path[2])
  checker_schedule = pd.read_excel(path[3])
  rows = len(sheet)
  checker_rows = 10 #checkers available for subway; will need to modify to select specific checkers
  wkd_graph = Graph(constants.DAY[0])
  sat_graph = Graph(constants.DAY[1])
  sun_graph = Graph(constants.DAY[2])
  #location for stations
  location_book = {}

  station_id_book = {}
  # build a map for stations and locations
  for i in range(len(station_loc)):
    station_id = str(station_loc.loc[i, 'GTFS Stop ID'])
    latitude = station_loc.loc[i, 'GTFS Latitude']
    longitude = station_loc.loc[i, 'GTFS Longitude']
    location_book[station_id] = [latitude, longitude]
  # build a map for station loc and station_rtif_id
  for i in range(len(station_ls)):
    station_loc_id = str(station_ls.loc[i, 'loc'])
    station_id = str(station_ls.loc[i, 'station_rtif_id'])
    station_id = station_id.split(',')[0]
    if not station_id_book.get(station_loc_id):
      station_id_book[station_loc_id]=station_id

  for i in tqdm(range(rows)):
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
    available_checkers = 0
    for j in range(0, checker_rows):
      if day == 'WKD':
        if ((int(checker_schedule.values[j,3])) - 100) >= begin_time:
          if (int(checker_schedule.values[j,2])) <= begin_time:
            available_checkers += 1
      elif day == 'SAT' and checker_schedule.values[j,5] == 'SUN - MON':
        if ((int(checker_schedule.values[j,3])) - 100) >= begin_time:
          if (int(checker_schedule.values[j,2])) <= begin_time:
            available_checkers += 1
      elif day == 'SUN' and checker_schedule.values[j,5] == 'FRI - SAT':
        if ((int(checker_schedule.values[j,3])) - 100) >= begin_time:
          if (int(checker_schedule.values[j,2])) <= begin_time:
            available_checkers += 1
        
    if available_checkers == 0:
      availability_priority = 1
    else:
      availability_priority = 1/available_checkers
    # mark the matrix
    for i in range(begin_entry, begin_entry+12):
      task_matrix[i, 0] = 1
    # get location of a station
    station_id = station_id_book.get(str(gate_id))
    if not station_id:
      loc = []
      print('Station ID for ' + name + ' not found.')
    loc = location_book.get(station_id)
    if not loc:
      loc = []
      print('Location for ' + name + ' not found.')

    task = Gate(name = name, boro = boro, loc = loc, routes = routes, gate_id = gate_id, begin_time = begin_time,
                task_matrix = task_matrix, day = day, comments = comments, availability_priority = availability_priority)

    # adding vertex to graph
    if task.day == constants.DAY[0]:
      wkd_graph.add_vertex(task)
    elif task.day == constants.DAY[1]:
      sat_graph.add_vertex(task)
    elif task.day == constants.DAY[2]:
      sun_graph.add_vertex(task)

  # normalize distance priority
  wkd_graph.normalize_distance_priority()
  sat_graph.normalize_distance_priority()
  sun_graph.normalize_distance_priority()

  #print and see the graphs 
  # wkd_graph.print()
  # sat_graph.print()
  # sun_graph.print()
  #wkd_graph.vertices[0][2].print()

  return wkd_graph, sat_graph, sun_graph


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--file_loc', default='NYCT FE Required Data/SFE SAMPLE210.xlsx', type=str)
  parser.add_argument('-s', '--station_loc', default='NYCT FE Required Data/station_location.csv', type=str)
  parser.add_argument('-i', '--station_id', default='NYCT FE Required Data/List of Stations and FCAs_v2.xlsx', type=str)
  parser.add_argument('-c', '--checker_schedule', default='NYCT FE Required Data/FE Checker List.xlsx', type=str)
  args = parser.parse_args()
  path = [args.file_loc, args.station_loc, args.station_id, args.checker_schedule]
  read(path)
  

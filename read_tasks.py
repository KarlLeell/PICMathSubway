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
import pickle
import constants
from scipy import stats



def read(path):
  print('Reading tasks: '+ path[0])
  print('Station locations reference: '+ path[1])
  print('Station booth id to rtif id reference: '+ path[2])
  print('Checker list: '+ path[3])
  sheet = pd.read_excel(path[0])
  station_loc = pd.read_csv(path[1])
  station_ls = pd.read_excel(path[2])
  checker_schedule = pd.read_excel(path[3])
  rows = len(sheet)
  checker_rows = len(checker_schedule) #checkers available for subway; will need to modify to select specific checkers
  wkd_graph = Graph(constants.DAY[0], constants.GRAPH_TYPE[1])
  sat_graph = Graph(constants.DAY[1], constants.GRAPH_TYPE[1])
  sun_graph = Graph(constants.DAY[2], constants.GRAPH_TYPE[1])
  # map from rtif id to locations
  location_book = {}
  # map from booth id to rtif id
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

  list_of_all_av_prio = []    
  for i in (range(rows)):
    available_checkers = 0
    day = sheet.values[i,2]
    begin_time = sheet.values[i,3]-100
    for j in range(19, 31):
      shift_end_time = int(checker_schedule.values[j,3]) - 100
      shift_start_time = int(checker_schedule.values[j,2]) + 100
      days_off = checker_schedule.values[j,5]
      if shift_end_time == -100:
        shift_end_time = 2300
      if shift_end_time == 0:
        shift_end_time = 2400
      if shift_start_time < shift_end_time:
        if day == 'WKD':
          if (shift_end_time - 100) >= begin_time:
            if shift_start_time <= begin_time:
              available_checkers += 1
        elif day == 'SAT' and days_off == 'SUN - MON':
          if (shift_end_time - 100) >= begin_time:
            if shift_start_time <= begin_time:
              available_checkers += 1
        elif day == 'SUN' and days_off == 'FRI - SAT':
          if (shift_end_time - 100) >= begin_time:
            if shift_start_time <= begin_time:
              available_checkers += 1
      elif shift_start_time > shift_end_time:
        if day == 'WKD':
          if shift_start_time <= begin_time:
            available_checkers += 1
          elif shift_start_time > begin_time:
            if (shift_end_time - 100) >= begin_time:
              available_checkers += 1
        elif day == 'SAT' and days_off == 'SUN - MON':
          if shift_start_time <= begin_time:
            available_checkers += 1
          elif shift_start_time > begin_time:
            if (shift_end_time - 100) >= begin_time:
              available_checkers += 1
        elif day == 'SUN' and days_off == 'FRI - SAT':
          if shift_start_time <= begin_time:
            available_checkers += 1
          elif shift_start_time > begin_time:
            if (shift_end_time - 100) >= begin_time:
              available_checkers += 1
      
    if available_checkers == 0:
      availability_priority = 1
    else:
      availability_priority = 1/available_checkers
    if availability_priority == 1:
      availability_priority += 1 #test buffer value
    list_of_all_av_prio.append(availability_priority)

  #normalized_av_prio = stats.zscore(list_of_all_av_prio).tolist()  
      
      
  for i in tqdm(range(rows)):
    booth_id = sheet.values[i, 1]
    day = sheet.values[i, 2]
    # begin_time has 24-hour format in form x00 where it actually means x:00
    # mod 24 because there are some 2400 to 2500 tasks
    begin_time = int(int(sheet.values[i, 3]) / 100 - 1)
    boro = sheet.values[i, 6]
    routes_str = str(sheet.values[i, 7])
    name = str(sheet.values[i, 8])
    routes = routes_str.split(',')
    task_matrix = np.zeros((24*12, 1))
    begin_entry = 12 * begin_time
    comments = sheet.values[i, 10]
    #availability_priority = normalized_av_prio[i]
    availability_priority = list_of_all_av_prio[i]
    # mark the matrix
    for i in range(begin_entry, begin_entry+12):
      task_matrix[i, 0] = 1
    # get location of a station
    station_id = station_id_book.get(str(booth_id))
    if not station_id:
      loc = []
      print('RTIF ID for ' + name + ' not found.')
    loc = location_book.get(station_id)
    if not loc:
      loc = [40.775594, -73.97641]
      print('Location for ' + name + ' not found.')

    task = Gate(name = name, boro = boro, loc = loc, routes = routes,
                booth_id = booth_id, begin_time = begin_time,
                task_matrix = task_matrix, day = day, comments = comments,
                availability_priority = availability_priority)

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
  wkd_graph.normalize_availability_priority()
  sat_graph.normalize_availability_priority()
  sun_graph.normalize_availability_priority()

  #print and see the graphs 
  # wkd_graph.print()
  # sat_graph.print()
  # sun_graph.print()
  #wkd_graph.vertices[0][0].print()
  #wkd_graph.vertices[2][5].print()

  with open('wkd_save.pkl','wb') as wkd, open('sat_save.pkl', 'wb') as sat, open('sun_save.pkl', 'wb') as sun:
    pickle.dump(wkd_graph, wkd)
    pickle.dump(sat_graph, sat)
    pickle.dump(sun_graph, sun)

  return wkd_graph, sat_graph, sun_graph


def read_failed_tasks(graph, file_name):
  tasks = pd.read_excel(file_name)
  for i in range(len(tasks)):
    booth_id = tasks.loc[i, 'booth_id']
    station_name = tasks.loc[i, 'sta']
    loc_str = tasks.loc[i, 'loc']
    loc = loc_str[1:len(loc_str)-1].split(',')
    day = tasks.loc[i, 'day']
    begin_time = tasks.loc[i, 'begin']
    boro = tasks.loc[i, 'boro']
    routes_str = tasks.loc[i, 'routes']
    routes = routes_str.split(',')
    comments = tasks.loc[i, 'comments_for_checker']
    new_gate = Gate(name = station_name, loc = loc, day = day, begin_time = begin_time, boro = boro,
              routes = routes, comments = comments, booth_id = booth_id)
    for g in graph:
      if g.day == day:
        g.add_vertex(new_gate)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--file_loc', default='NYCT FE Required Data/SFE SAMPLE210.xlsx', type=str)
  parser.add_argument('-s', '--station_loc', default='NYCT FE Required Data/station_location.csv', type=str)
  parser.add_argument('-i', '--station_id', default='NYCT FE Required Data/List of Stations and FCAs_v2.xlsx', type=str)
  parser.add_argument('-c', '--checker_schedule', default='NYCT FE Required Data/FE Checker List ASSIGNED.xlsx', type=str)
  args = parser.parse_args()
  path = [args.file_loc, args.station_loc, args.station_id, args.checker_schedule]
  read(path)
  

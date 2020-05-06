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
  print('Special sample: '+ path[4])
  sheet = pd.read_excel(path[0])
  station_loc = pd.read_csv(path[1])
  station_ls = pd.read_excel(path[2])
  checker_schedule = pd.read_excel(path[3])
  special = pd.read_excel(path[4])
  rows = len(sheet)
  special_rows = len(special)
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

  # build a 3*24 map where each entry represents the number of checkers
  #   available at that time
  availability_book = {}
  for i in range(3):
    availability_book[i] = {}
    for j in range(24):
      availability_book[i][j] = 0
  for i in range(19, 31):
    shift_end_time = int(int(checker_schedule.values[i,3]) / 100 - 1)
    shift_start_time = int(int(checker_schedule.values[i,2]) / 100 + 1)
    days_off = checker_schedule.values[i,5]
    if days_off == 'FRI - SAT':
      for j in range(shift_start_time, shift_end_time):
        availability_book[2][j] = availability_book[2][j] + 1
    elif days_off == 'SAT - SUN':
      for j in range(shift_start_time, shift_end_time):
        availability_book[0][j] = availability_book[0][j] + 1
    elif days_off == 'SUN - MON':
      for j in range(shift_start_time, shift_end_time):
        availability_book[1][j] = availability_book[1][j] + 1
    else:
        print('Unrecognized days off: ' + days_off)
  wkd_graph.availability_book = availability_book
  sat_graph.availability_book = availability_book
  sun_graph.availability_book = availability_book

      
  for i in tqdm(range(rows)):
    sample_id = sheet.loc[i, 'sample_id']
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
    # calculate availability priority
    if day == constants.DAY[0]:
      i = 0
    elif day == constants.DAY[1]:
      i = 1
    elif day == constants.DAY[2]:
      i = 2
    available_checkers = availability_book[i][begin_time]
    if available_checkers == 0:
      availability_priority = 1
    else:
      availability_priority = 1/available_checkers
    if availability_priority == 1:
      availability_priority += 1 #test buffer value

    # mark the matrix
    for i in range(begin_entry, begin_entry+12):
      task_matrix[i, 0] = 1
    # get location of a station
    station_id = station_id_book.get(str(booth_id))
    if not station_id:
      loc = [0, 0]
      print('RTIF ID for ' + name + ' not found.')
    loc = location_book.get(station_id)
    if not loc:
      loc = [0, 0]
      print('Location for ' + name + ' not found.')

    task = Gate(name = name, boro = boro, loc = loc, routes = routes,
                sample_id = sample_id, booth_id = booth_id, begin_time = begin_time,
                task_matrix = task_matrix, day = day, comments = comments,
                availability_priority_holder = availability_priority)

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
  
  
  #read special sample
  for i in range(special_rows):
    sample_id = special.loc[i, 'sample_id']
    booth_id = special.values[i, 1]
    day = special.values[i, 3]
    time_period = special.values[i, 9]
    boro = special.values[i, 5]
    routes_str = str(special.values[i, 6])
    name = str(special.values[i, 4])
    routes = routes_str.split(',')
    comments = special.values[i, 8]
    # get location of a station
    station_id = station_id_book.get(str(booth_id))
    if not station_id:
      loc = []
      print('RTIF ID for ' + name + ' not found.')
    loc = location_book.get(station_id)
    if not loc:
      loc = [40.775594, -73.97641]
      print('Location for ' + name + ' not found.')
      
    special_task = Gate(name = name, boro = boro, loc = loc, routes = routes,
                          sample_id = sample_id, booth_id = booth_id, day = day,
                          comments = comments, task_type = constants.TASK_TYPE[2])
    
    if day == constants.DAY[0]:
      if time_period == 'AM':
        wkd_graph.am_special_tasks.append(special_task)
      elif time_period == 'PM':
        wkd_graph.pm_special_tasks.append(special_task)
    elif day == constants.DAY[1]:
      if time_period == 'AM':
        sat_graph.am_special_tasks.append(special_task)
      elif time_period == 'PM':
        sat_graph.pm_special_tasks.append(special_task)
    elif day == constants.DAY[2]:
      if time_period == 'AM':
        sun_graph.am_special_tasks.append(special_task)
      elif time_period == 'PM':
        sun_graph.pm_special_tasks.append(special_task)
 
  
  with open('wkd_save.pkl','wb') as wkd, open('sat_save.pkl', 'wb') as sat, open('sun_save.pkl', 'wb') as sun:
    pickle.dump(wkd_graph, wkd)
    pickle.dump(sat_graph, sat)
    pickle.dump(sun_graph, sun)

  return wkd_graph, sat_graph, sun_graph


def read_failed_tasks(graph, file_name):
  tasks = pd.read_excel(file_name)
  for i in range(len(tasks)):
    sample_id = tasks.loc[i, 'sample_id']
    booth_id = tasks.loc[i, 'booth_id']
    station_name = tasks.loc[i, 'sta']
    loc_str = tasks.loc[i, 'loc']
    loc = loc_str[1:len(loc_str)-1].split(',')
    day = tasks.loc[i, 'day']
    begin_time = int(tasks.loc[i, 'begin'] / 100)
    boro = tasks.loc[i, 'boro']
    routes_str = tasks.loc[i, 'routes']
    routes = routes_str.split(',')
    comments = tasks.loc[i, 'comments_for_checker']
    new_gate = Gate(name = station_name, loc = loc, day = day, sample_id = sample_id,
                      begin_time = begin_time, boro = boro, routes = routes,
                      comments = comments, booth_id = booth_id,
                      task_type = constants.TASK_TYPE[1])
    for g in graph:
      if g.day == day:
        daytype = constants.DAY.index(day)
        available_checkers = g.availability_book[daytype][new_gate.begin_time]
        if available_checkers != 0:
          new_gate.availability_priority_holder = 1 / available_checkers
        else:
          new_gate.availability_priority_holder = 1
        if available_checkers == 1:
          new_gate.availability_priority_holder = 2
        g.add_vertex(new_gate)
  for g in graph:
    g.normalize_distance_priority()
    g.normalize_availability_priority()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--file_loc', default='NYCT FE Required Data/SFE SAMPLE210.xlsx', type=str)
  parser.add_argument('-s', '--station_loc', default='NYCT FE Required Data/station_location.csv', type=str)
  parser.add_argument('-i', '--station_id', default='NYCT FE Required Data/List of Stations and FCAs_v2.xlsx', type=str)
  parser.add_argument('-c', '--checker_schedule', default='NYCT FE Required Data/FE Checker List ASSIGNED.xlsx', type=str)
  parser.add_argument('-p', '--special', default='NYCT FE Required Data/SFE Special AM-PM.xlsx', type=str)
  args = parser.parse_args()
  path = [args.file_loc, args.station_loc, args.station_id, args.checker_schedule, args.special]
  read(path)
  

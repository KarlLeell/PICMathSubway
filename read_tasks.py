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

DAYTYPE = ['WKD', 'SAT', 'SUN']

def main(args):
  print(args.file_loc)
  sheet = pd.read_excel(args.file_loc)
  rows = len(sheet)
  wkd_graph = Graph(day = constants.DAY[0])
  sat_graph = Graph(day = constants.DAY[1])
  sun_graph = Graph(day = constants.DAY[2])

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

    task = Gate(name = name, boro = boro, routes = routes, gate_id = gate_id, begin_time = begin_time,
                task_matrix = task_matrix, day = day, comments = comments)

    # adding vertex to graph
    if task.day == DAYTYPE[0]:
      wkd_graph.add_vertex(task)
    elif task.day == DAYTYPE[1]:
      sat_graph.add_vertex(task)
    elif task.day == DAYTYPE[2]:
      sun_graph.add_vertex(task)

  # print and see the graphs
  sat_graph.print()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('file_loc', type = str, default = 'NYCT FE Required Data/List of Stations and FCAs.xlsx')
  args = parser.parse_args()
  main(args)

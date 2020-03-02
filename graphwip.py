import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def weighted_adjmatrix(adjlist, nodes):
    '''Returns a (weighted) adjacency matrix as a NumPy array, I don't think we need this but it could be useful.'''
    matrix = []
    for node in nodes:
        weights = {endnode:int(weight)
                   for w in adjlist.get(node, {})
                   for endnode, weight in w.items()}
        matrix.append([weights.get(endnode, 0) for endnode in nodes])
    matrix = np.array(matrix)
    return matrix + matrix.transpose()
    
    
H=nx.Graph(adjmatrix)
plt.title('title')
nx.draw(H, with_labels=True, node_size=100, node_color="skyblue")
plt.show()








#==========================================
# Title:  Station Class
# Author: NYUPICMathSubwayGroup
# Date:   2020.02.24
# Comment:
#==========================================



class Station:

  def __init__(self, name = '', loc = [0,0], boro = '', routes = []):
    # station name
    self.name_ = name
    # location of the staion in terms of geographic coordinate system, [longitude, latitude]
    self.loc_ = loc
    # district: M = Manhattan, Q = Queens, BK = Brooklyn
    self.boro_ = boro
    # routes of subways in this station
    self.routes_ = routes

  # return the location
  def abs_loc(self):
    return self.loc_

  # update station info
  def set_station(self, name = '', loc = [0,0], boro = '', routes = []):
    self.name_ = name
    self.loc_ = loc
    self.boro_ = boro
    self.routes_ = routes

  # print the station info
  def print(self):
    print('Station Name: ' + self.name_) 
    print('Station Location: ' + str(self.loc_))
    print('Station Boro: ' + self.boro_)
    print('Station Routes: ' + str(self.routes_))




##from station import Station

class Gate(Station):
  def __init__(self, name = '', loc = [0,0], boro = '', routes = [], gate_id = '', task_matrix = np.zeros((24*12, 1)),
    day = '', neighbors = [], edge_dist_tt = [], comments = ''):
    # inherited attribute
    #self.name_ = name
    #self.loc_ = loc
    #self.boro_ = boro
    #self.routes_ = routes
    super().__init__(name, loc, boro, routes)
    # self attributes
    self.gate_id_ = gate_id
    self.task_matrix_ = task_matrix
    self.day_ = day
    self.neighbors_ = neighbors
    self.edge_dist_tt_ = edge_dist_tt
    self.comments_ = comments

  # def abs_loc(self):

  def find_neighbors(self):
    pass
  def calc_edge_dist_tt(self):
    pass

  def print(self):
    super().print()
    print('Gate ID: ' + self.gate_id_) 
    print('Day: ' + str(self.day_))


##C:\Users\David\Desktop\NYCT FE Required Data\SFE SAMPLE210

#==========================================
# Title:  Test Station Class
# Author: NYUPICMathSubwayGroup
# Date:   2020.02.24
# Comment:Need pandas to run this test
#==========================================


import argparse
##from Station import Station

def main():
  print("C:/Users/David/Desktop/NYCT FE Required Data/SFE SAMPLE210.xlsx")
  sheet = station_file = pd.read_excel("C:/Users/David/Desktop/NYCT FE Required Data/SFE SAMPLE210.xlsx")
  rows = len(sheet)
  stations = []
  gates = []
  for i in range(0, rows):
    # the location in file is actually the entry i think
    gate_id = sheet.values[i,1]
    day = sheet.values[i,2]
    begin_time = sheet.values[i,3]
    name = sheet.values[i, 8]
    boro = sheet.values[i, 6]
    routes = str(sheet.values[i, 7]).split(",")
    task_matrix = np.zeros((24*12, 1))
    begin_entry = 12*int(begin_time) % 100
    for i in range(begin_entry, begin_entry+12):
      task_matrix[i,0] = 1
    station = Station(name = name, boro = boro, routes = routes)
    gate = Gate(gate_id = gate_id, day = day,
                name = name, boro = boro, routes = routes)
    stations.append(station)
    gates.append(gate)
##  for n in range(0,len(stations)):
##    stations[n].print()
##    print()
  for n in range(0,len(gates)):
    gates[n].print()
    print()

  print('Number of stations:',len(stations))

    
main()
##if __name__ == '__main__':
##  parser = argparse.ArgumentParser()
##  parser.add_argument('file_loc', type = str, default = 'NYCT FE Required Data/List of Stations and FCAs')
##  args = parser.parse_args()
##  main(args)




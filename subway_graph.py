#==========================================
# Title:  Reading into graph
# Author: NYUPICMathSubwayGroup
# Date:   2020.03.02
# Comment:
#==========================================

import numpy as np
from gate import Gate
import constants
from queue import Queue
from scipy import stats

class Graph():

  def __init__(self, day = constants.DAY[0]):
    self.day = day
    self.empty_vertex = Gate(name = 'Root', begin_time = 0, day = self.day)
    #self.lic_vertex = Gate(name = 'LIC', begin_time = 0, day = self.day)

    # list of lists of tasks at all 24 hours
    self.vertices = []
    for i in range(24):
      self.vertices.append([])
      skip_empty_vertexM = Gate(name = 'SkipM', begin_time = i, boro = 'M', day = self.day)
      skip_empty_vertexQ = Gate(name = 'SkipQ', begin_time = i, boro = 'Q', day = self.day)
      skip_empty_vertexBK = Gate(name = 'SkipBK', begin_time = i, boro = 'BK', day = self.day)
      skip_empty_vertexBX = Gate(name = 'SkipBX', begin_time = i, boro = 'BX', day = self.day)
      lic_empty_vertex = Gate(name = 'LIC', begin_time = i, day = self.day, loc = [40.733997064, -73.935996256])

      self.vertices[i].append(lic_empty_vertex)
      self.vertices[i].append(skip_empty_vertexM)
      self.vertices[i].append(skip_empty_vertexQ)
      self.vertices[i].append(skip_empty_vertexBK)
      self.vertices[i].append(skip_empty_vertexBX)

      # connect skipping vertices at current layer to that at next layer
      if i != 0:
        self.vertices[i-1][0].neighbors.append(lic_empty_vertex)
        self.vertices[i-1][0].neighbors.append(skip_empty_vertexM)
        self.vertices[i-1][0].neighbors.append(skip_empty_vertexQ)
        self.vertices[i-1][0].neighbors.append(skip_empty_vertexBK)
        self.vertices[i-1][0].neighbors.append(skip_empty_vertexBX)
        self.vertices[i-1][1].neighbors.append(skip_empty_vertexM)
        self.vertices[i-1][2].neighbors.append(skip_empty_vertexQ)
        self.vertices[i-1][3].neighbors.append(skip_empty_vertexBK)
        self.vertices[i-1][4].neighbors.append(skip_empty_vertexBX)
        for j in range(5):
          # distance between skipping vertices connecting each other is 0
          self.vertices[i-1][j].edge_dist_tt.append(0)
          self.vertices[i-1][j].dist_prio.append(0)
      # connect starting empty vertices with skipping vertex at the first layer
      else:
        self.empty_vertex.neighbors.append(lic_empty_vertex) 
        self.empty_vertex.neighbors.append(skip_empty_vertexM) 
        self.empty_vertex.neighbors.append(skip_empty_vertexQ) 
        self.empty_vertex.neighbors.append(skip_empty_vertexBK) 
        self.empty_vertex.neighbors.append(skip_empty_vertexBX)
        for j in range(5):
          self.empty_vertex.edge_dist_tt.append(0)
          self.empty_vertex.dist_prio.append(0)

  def add_vertex(self, vertex):
    # the vertex should be an instance of Gate
    if type(vertex) != Gate:
      print('Input vertex should be an instance of Gate')
      raise Exception('Input vertex should be an instance of Gate')

    time = vertex.begin_time
    self.vertices[time].append(vertex)
    if time == 0:
      # connect starting empty vertex with this vertex
      self.empty_vertex.neighbors.append(vertex)
      self.empty_vertex.edge_dist_tt.append(0)
      self.empty_vertex.dist_prio.append(0)
    else:
      # connect vertices on last layer and this vertex
      for prev_vertex in self.vertices[time-1]:
        # do not connect skipping vertices not in the same boro
        if 'Skip' in prev_vertex.name and prev_vertex.name != 'Skip' + vertex.boro:
          continue
        prev_vertex.neighbors.append(vertex)
        # set this to be 5 for now
        if 'Skip' in prev_vertex.name:
          prev_vertex.edge_dist_tt.append(0)
          prev_vertex.dist_prio.append(0)
        else:
          distance = prev_vertex.calc_travel_time(vertex)
          prev_vertex.edge_dist_tt.append(distance)
          prev_vertex.dist_prio.append(0 - distance)
        
    if time != 23:
      # connect this vertex and vertices on next layer
      for next_vertex in self.vertices[time+1]:
        if 'Skip' in next_vertex.name and next_vertex.name != 'Skip' + vertex.boro:
            continue
        vertex.neighbors.append(next_vertex)
        if 'Skip' in next_vertex.name:
          vertex.edge_dist_tt.append(0)
          vertex.dist_prio.append(0)
        else:
          distance = vertex.calc_travel_time(next_vertex)
          vertex.edge_dist_tt.append(distance)
          vertex.dist_prio.append(0 - distance)

  def normalize_distance_priority(self):
    list_of_all_distances = []
    number_of_elements = []
    # TODO: This is a very slow implementation, should in the future switch to Queue
    q = []
    q_next = []
    q.append(self.empty_vertex)
    while len(q) != 0:
      for vertex in q:
        #print('Calc for ' + vertex.name)
        list_of_all_distances.extend(vertex.dist_prio)
        number_of_elements.append(len(vertex.dist_prio))
        if q_next == []:
          q_next.extend(vertex.neighbors)
      q = q_next[::]
      q_next = []
    normalized_prio = stats.zscore(list_of_all_distances).tolist()
    #print('Done calc')
    index = 0
    current = 0
    q = []
    q_next = []
    q.append(self.empty_vertex)
    while len(q) != 0:
      for vertex in q:
        #print('Recover for ' + vertex.name)
        vertex.dist_prio = normalized_prio[current:current+number_of_elements[index]][::]
        if q_next == []:
          q_next.extend(vertex.neighbors)
        current = current + number_of_elements[index]
        index = index + 1
      q = q_next[::]
      q_next = []
    #print('Done recover')


  def print(self):
    print('Graph for ' + self.day)
    for lists in self.vertices:
      print('Begin Time: ' + str(lists[0].begin_time) + '.\tTasks: [', end='')
      for gate in lists:
        if gate != lists[len(lists)-1]:
          print(gate.name, end = ', ')
        else:
          print(gate.name, end = '')
      print(']')
    print('End Graph for ' + self.day)


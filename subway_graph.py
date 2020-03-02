#==========================================
# Title:  
# Author: 
# Date:   
# Comment:
#==========================================

import numpy as np
from gate import Gate
import constants
import copy as cp

class Graph():

  def __init__(self, day = constants.DAY[0]):
    self.empty_vertex = Gate(name = 'Skip', begin_time = 0, day = day)
    # list of lists of tasks at all 24 hours
    self.vertices = []
    for i in range(24):
      self.vertices.append([])
      temp_empty_vertex = Gate(name = 'Skip', begin_time = i, day = day)
      self.vertices[i].append(temp_empty_vertex)
      # connect skipping vertex at current layer to that at next layer
      if i != 0:
        self.vertices[i-1][0].neighbors.append(temp_empty_vertex)
        self.vertices[i-1][0].edge_dist_tt.append(0)
      # connect starting empty vertex with skipping vertex at the first layer
      else:
        self.empty_vertex.neighbors.append(temp_empty_vertex) 
        self.empty_vertex.edge_dist_tt.append(0)

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
    else:
      # connect vertices on last layer and this vertex
      for prev_vertex in self.vertices[time-1]:
        prev_vertex.neighbors.append(vertex)
        # set this to be 5 for now
        prev_vertex.edge_dist_tt.append(5)
        
    if time != 23:
      # connect this vertex and vertices on next layer
      for next_vertex in self.vertices[time+1]:
        vertex.neighbors.append(next_vertex)
        vertex.edge_dist_tt.append(5)

  def print(self):
    for lists in self.vertices:
      print('[', end='')
      for gate in lists:
        if gate != lists[len(lists)-1]:
          print(gate.name, end = ', ')
        else:
          print(gate.name, end = '')
      print(']')


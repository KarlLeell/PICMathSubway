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
      lic_empty_vertex = Gate(name = 'LIC', begin_time = i, day = self.day,
                              loc = [constants.LIC_LATITUDE, constants.LIC_LONGITUDE])
      self.vertices[i].append(lic_empty_vertex)
      self.vertices[i].append(skip_empty_vertexM)
      self.vertices[i].append(skip_empty_vertexQ)
      self.vertices[i].append(skip_empty_vertexBK)
      self.vertices[i].append(skip_empty_vertexBX)
      # [0 LIC, 1 M, 2 Q, 3 BK, 4 BX]
      # connect skipping vertices at current layer to that at next layer
      if i != 0:
        '''
        self.vertices[i-1][0].neighbors.append(lic_empty_vertex)
        self.vertices[i-1][0].neighbors.append(skip_empty_vertexM)
        self.vertices[i-1][0].neighbors.append(skip_empty_vertexQ)
        self.vertices[i-1][0].neighbors.append(skip_empty_vertexBK)
        self.vertices[i-1][0].neighbors.append(skip_empty_vertexBX)
        '''
        self.vertices[i-1][1].neighbors.append(lic_empty_vertex)
        self.vertices[i-1][1].neighbors.append(skip_empty_vertexM)
        
        self.vertices[i-1][2].neighbors.append(lic_empty_vertex)
        self.vertices[i-1][2].neighbors.append(skip_empty_vertexQ)
        
        self.vertices[i-1][3].neighbors.append(lic_empty_vertex)
        self.vertices[i-1][3].neighbors.append(skip_empty_vertexBK)
        
        self.vertices[i-1][4].neighbors.append(lic_empty_vertex)
        self.vertices[i-1][4].neighbors.append(skip_empty_vertexBX)
        '''
        for j in range(5):
          self.vertices[i-1][0].edge_dist_tt.append(0)
          self.vertices[i-1][0].dist_prio.append(0)
        '''
        for j in range(4):
          # distance between skipping vertices connecting each other is 0
          self.vertices[i-1][j+1].edge_dist_tt.append(0) # skip to lic is 0
          self.vertices[i-1][j+1].dist_prio.append(0) # skip to lic is 0
          self.vertices[i-1][j+1].edge_dist_tt.append(0) # skip to skip is 0
          self.vertices[i-1][j+1].dist_prio.append(0) # skip to skip is 0

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

  def find_vertex(self, booth_id, begin_time):
    for vertex in self.vertices[begin_time]:
      if vertex.booth_id == booth_id and vertex.begin_time == begin_time:
        return vertex
    # if not found return none
    return None

  def delete_vertex(self, vertex=None, booth_id='', begin_time=0):
    if not vertex:
      vertex = self.find_vertex(booth_id, begin_time)
      if not vertex:
        # return false if not vertex found
        return False
    # return false if not a Gate object
    if type(vertex) != type(self.empty_vertex):
      return False

    booth_id = vertex.booth_id
    begin_time = vertex.begin_time

    # remove edges to this vertex
    if vertex.begin_time != 0:
      for prev_vertex in self.vertices[vertex.begin_time - 1]:
        for i in range(len(prev_vertex.neighbors)):
          if prev_vertex.neighbors[i].booth_id == booth_id:
            prev_vertex.neighbors.pop(i)
            prev_vertex.edge_dist_tt.pop(i)
            prev_vertex.dist_prio.pop(i)
            break
    else:
      for i in range(len(self.empty_vertex.neighbors)):
        if self.empty_vertex.neighbors[i].booth_id == booth_id:
          self.empty_vertex.neighbors.pop(i)
          self.empty_vertex.edge_dist_tt.pop(i)
          self.empty_vertex.dist_prio.pop(i)
          break

    # remove this vertex from list
    self.vertices[begin_time].remove(vertex)

    return True

  def normalize_distance_priority(self):
    list_of_all_distances = []
    number_of_elements = []
    q = []
    for l in self.vertices:
      for vertex in l:
        #print('Calc for ' + vertex.name)
        list_of_all_distances.extend(vertex.dist_prio)
        number_of_elements.append(len(vertex.dist_prio))
        q.append(vertex)
    normalized_prio = stats.zscore(list_of_all_distances).tolist()
    #print('Done calc')
    current = 0
    for i in range(len(q)):
      vertex = q[i]
      num_ele = number_of_elements[i]
      #print('Recover for ' + vertex.name)
      vertex.dist_prio = normalized_prio[current:current+num_ele][::]
      current = current + num_ele
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


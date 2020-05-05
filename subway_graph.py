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
import random



class Graph():

  def __init__(self, day = constants.DAY[0], graph_type = constants.GRAPH_TYPE[0]):
    self.day = day
    self.empty_vertex = Gate(name = 'Root', begin_time = 0, day = self.day)
    self.graph_type = graph_type
    self.am_special_tasks = []
    self.pm_special_tasks = []
    self.availability_book = None

    #self.lic_vertex = Gate(name = 'LIC', begin_time = 0, day = self.day)

    # list of lists of tasks at all 24 hours
    self.vertices = []

    if self.graph_type == constants.GRAPH_TYPE[0]:
        self.naive_init()
    elif self.graph_type == constants.GRAPH_TYPE[1]:
        self.fine_init()

  def naive_init(self):
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
        self.vertices[i-1][0].neighbors.append(skip_empty_vertexM)
        self.vertices[i-1][0].neighbors.append(skip_empty_vertexQ)
        self.vertices[i-1][0].neighbors.append(skip_empty_vertexBK)
        self.vertices[i-1][0].neighbors.append(skip_empty_vertexBX)

        for j in range(4):
          self.vertices[i-1][j+1].neighbors.append(lic_empty_vertex)
          self.vertices[i-1][j+1].neighbors.append(skip_empty_vertexM)
          self.vertices[i-1][j+1].neighbors.append(skip_empty_vertexQ)
          self.vertices[i-1][j+1].neighbors.append(skip_empty_vertexBK)
          self.vertices[i-1][j+1].neighbors.append(skip_empty_vertexBX)

        for j in range(4):
          # distance between lic to skipping vertices is 0
          self.vertices[i-1][0].edge_dist_tt.append(0)
          self.vertices[i-1][0].dist_prio.append(0)
          # distance between skipping vertices connecting each other is 0
          for k in range(5):
            self.vertices[i-1][j+1].edge_dist_tt.append(0)
            self.vertices[i-1][j+1].dist_prio.append(0)

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

  def fine_init(self):
    for i in range(24):
      self.vertices.append([])
      lic_empty_vertex = Gate(name = 'LIC', begin_time = i, day = self.day,
                              loc = [constants.LIC_LATITUDE, constants.LIC_LONGITUDE])
      skip_empty_vertex = Gate(name='GSkip', begin_time = i, day = self.day)
      self.vertices[i].append(lic_empty_vertex)
      self.vertices[i].append(skip_empty_vertex)
      
      if i != 0:
        # connect neighbors
        self.vertices[i-1][0].neighbors.append(lic_empty_vertex)
        self.vertices[i-1][0].neighbors.append(skip_empty_vertex)
        self.vertices[i-1][1].neighbors.append(lic_empty_vertex)
        self.vertices[i-1][1].neighbors.append(skip_empty_vertex)
        # add distances of 0
        self.vertices[i-1][0].edge_dist_tt.append(0)
        self.vertices[i-1][0].edge_dist_tt.append(0)
        self.vertices[i-1][1].edge_dist_tt.append(0)
        self.vertices[i-1][1].edge_dist_tt.append(0)
        # add distance priority
        self.vertices[i-1][0].dist_prio.append(0)
        self.vertices[i-1][0].dist_prio.append(0)
        self.vertices[i-1][1].dist_prio.append(0)
        self.vertices[i-1][1].dist_prio.append(0)
      else:
        self.empty_vertex.neighbors.append(lic_empty_vertex)
        self.empty_vertex.neighbors.append(skip_empty_vertex)
        self.empty_vertex.edge_dist_tt.append(0)
        self.empty_vertex.edge_dist_tt.append(0)
        self.empty_vertex.dist_prio.append(0)
        self.empty_vertex.dist_prio.append(0)
      if i == 23:
        # connect to layer 0 to form a circular graph
        self.vertices[i][0].neighbors.append(self.vertices[0][0])
        self.vertices[i][0].neighbors.append(self.vertices[0][1])
        self.vertices[i][1].neighbors.append(self.vertices[0][0])
        self.vertices[i][1].neighbors.append(self.vertices[0][1])
        # add distances of 0
        self.vertices[i][0].edge_dist_tt.append(0)
        self.vertices[i][0].edge_dist_tt.append(0)
        self.vertices[i][1].edge_dist_tt.append(0)
        self.vertices[i][1].edge_dist_tt.append(0)
        # add distance priority
        self.vertices[i][0].dist_prio.append(0)
        self.vertices[i][0].dist_prio.append(0)
        self.vertices[i][1].dist_prio.append(0)
        self.vertices[i][1].dist_prio.append(0)

  def add_vertex(self, vertex):
    if self.graph_type == constants.GRAPH_TYPE[0]:
      self.naive_add(vertex)
    elif self.graph_type == constants.GRAPH_TYPE[1]:
      self.fine_add(vertex)

  def naive_add(self, vertex):
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

  def fine_add(self, vertex):

    self.fine_add_aux(vertex)
    task_empty_vertex = Gate(name = 'Skip_'+vertex.name, boro=vertex.boro,
                              loc = [vertex.loc[0], vertex.loc[1]], day = vertex.day,
                              booth_id = vertex.booth_id,
                              begin_time = (vertex.begin_time+1)%24)
    self.fine_add_aux(task_empty_vertex)

  def fine_add_aux(self, vertex):
    # the vertex should be an instance of Gate
    if type(vertex) != Gate:
      print('Input vertex should be an instance of Gate')
      raise Exception('Input vertex should be an instance of Gate')

    time = vertex.begin_time % 24
    self.vertices[time].append(vertex)

    if time == 0:
      # connect starting empty vertex with this vertex
      self.empty_vertex.neighbors.append(vertex)
      self.empty_vertex.edge_dist_tt.append(0)
      self.empty_vertex.dist_prio.append(0)

    # if vertex is a private skipping vertex
    if 'Skip_' in vertex.name:
      for prev_vertex in self.vertices[(time-1) % 24]:
        # connect its private task to it
        if 'Skip_' + prev_vertex.name == vertex.name and prev_vertex.booth_id == vertex.booth_id:
          prev_vertex.neighbors.append(vertex)
          prev_vertex.edge_dist_tt.append(0)
          prev_vertex.dist_prio.append(0)
        # do not connect anything else
        else:
          continue
      for next_vertex in self.vertices[(time+1) % 24]:
        # connect skipping to general skipping
        if 'GSkip' in next_vertex.name:
          vertex.neighbors.append(next_vertex)
          vertex.edge_dist_tt.append(0)
          vertex.dist_prio.append(0)
        # do not connect skipping to skipping
        elif 'Skip_' in next_vertex.name:
          continue
        else:
          vertex.neighbors.append(next_vertex)
          distance = vertex.calc_travel_time(next_vertex)
          vertex.edge_dist_tt.append(distance)
          vertex.dist_prio.append(0 - distance)
    # if vertex is a real task
    else:
      for prev_vertex in self.vertices[(time-1) % 24]:
        if 'GSkip' in prev_vertex.name:
          prev_vertex.neighbors.append(vertex)
          prev_vertex.edge_dist_tt.append(0)
          prev_vertex.dist_prio.append(0)
        else:
          prev_vertex.neighbors.append(vertex)
          distance = prev_vertex.calc_travel_time(vertex)
          prev_vertex.edge_dist_tt.append(distance)
          prev_vertex.dist_prio.append(0 - distance)
      for next_vertex in self.vertices[(time+1) % 24]:
        if 'GSkip' in next_vertex.name:
          continue
        elif 'Skip_' in next_vertex.name:
          if 'Skip_' + vertex.name == next_vertex.name and vertex.booth_id == next_vertex.booth_id:
            vertex.neighbors.append(next_vertex)
            vertex.edge_dist_tt.append(0)
            vertex.dist_prio.append(0)
          else:
            continue
        else:
          vertex.neighbors.append(next_vertex)
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
        # return false if no vertex found
        return False
    # return false if not a Gate object
    if type(vertex) != type(self.empty_vertex):
      return False

    if self.graph_type == constants.GRAPH_TYPE[0]:
      return self.naive_del_vertex(vertex)
    elif self.graph_type == constants.GRAPH_TYPE[1]:
      return self.fine_del_vertex(vertex)

  def naive_del_vertex(self, vertex):
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
      for prev_vertex in self.vertices[23]:
        for i in range(len(prev_vertex.neighbors)):
          if prev_vertex.neighbors[i].booth_id == booth_id:
            prev_vertex.neighbors.pop(i)
            prev_vertex.edge_dist_tt.pop(i)
            prev_vertex.dist_prio.pop(i)
            break

    # remove this vertex from list
    self.vertices[begin_time].remove(vertex)

    return True

  def fine_del_vertex(self, vertex):
    name = vertex.name
    if 'GSkip' not in name and 'Skip_' not in name and 'LIC' not in name:
      for next_vertex in vertex.neighbors:
        if 'Skip_' in next_vertex.name:
          skip_vertex = next_vertex
          break
      # this is not actually necessary in current implementation, as the only
      #   vertex that points to a private skipping vertex will be deleted too
      #   we can simply remove it from the list of vertices
      self.naive_del_vertex(skip_vertex)
    self.naive_del_vertex(vertex)
    
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

  def normalize_availability_priority(self):
    list_of_all_avail = []
    for l in self.vertices:
      for vertex in l:
        list_of_all_avail.append(vertex.availability_priority_holder)
    normalized_avail = stats.zscore(list_of_all_avail).tolist()
    index = 0
    for l in self.vertices:
      for vertex in l:
        vertex.availability_priority = normalized_avail[index]
        index = index + 1

  
  def sparsity_check(self):
    sparse_indices = []
    for layer in self.vertices:
      real_tasks = 0
      for gate in layer:
        if 'Skip' not in gate.name and 'LIC' not in gate.name:
          real_tasks += 1
      if real_tasks <= 2:
        sparse_indices.append(self.vertices.index(layer))
    return sparse_indices
  
  
  def add_special_task(self, layer):
    if layer < 12:
      if len(self.am_special_tasks) == 0:
        return None
      else:
        i = random.randint(0,len(self.am_special_tasks)-1)
        vertex = self.am_special_tasks[i]
        self.am_special_tasks.pop(i)
    elif layer >= 12:
      if len(self.pm_special_tasks) == 0:
        return None
      else:
        i = random.randint(0,len(self.pm_special_tasks)-1)
        vertex = self.pm_special_tasks[i]
        self.pm_special_tasks.pop(i)
    vertex.begin_time = layer
    available_checkers = self.availability_book[constants.DAY.index(self.day)][layer]
    if available_checkers == 0:
      vertex.availability_priority_holder = 1
    else:
      vertex.availability_priority_holder = 1/available_checkers
    if vertex.availability_priority_holder == 1:
      vertex.availability_priority_holder += 1
    # print("Special Task:\n")
    # vertex.print()
    self.add_vertex(vertex)
    
    
  def add_special_sample(self):
    sparse_indices = self.sparsity_check()
    print("Sparse Indices: " + str(sparse_indices))
    for layer in sparse_indices:
      self.add_special_task(layer)
      print("special sample added to " + str(layer))
      # self.add_special_task(layer)
    self.normalize_availability_priority()
  
  
  
  
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


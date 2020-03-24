#==========================================
# Title:  Gate Class
# Author: NYUPICMathSubwayGroup
# Date:   2020.03.02
# Comment:
#==========================================

import numpy as np
from station import Station
import math
import constants

class Gate(Station):


  def __repr__(self):
    return self.name
  def __str__(self):
    return self.name


  def __init__(self, name = '', loc = None, boro = '', routes = None, gate_id = '', begin_time = 0,
                task_matrix = np.zeros((24*12, 1)), day = '', neighbors = None, edge_dist_tt = None, comments = '', value = 0):
    # inherited attribute
    #self.name_ = name
    #self.loc_ = loc
    #self.boro_ = boro
    #self.routes_ = routes
    super().__init__(name, loc, boro, routes)
    # self attributes
    self.gate_id = gate_id
    self.begin_time = begin_time
    self.task_matrix = task_matrix
    self.day = day
    self.neighbors = neighbors if neighbors is not None else []
    self.edge_dist_tt = edge_dist_tt if edge_dist_tt is not None else []
    self.comments = comments
    self.finished = False
    self.value = value


  # def abs_loc(self):

  def find_neighbors(self):
    return self.neighbors

  def calc_edge_dist_tt(self, dst_gate):
    sta_loc = self.abs_loc()
    dst_loc = dst_gate.abs_loc()
    dlat = math.radians(math.radians(sta_loc[0]) - math.radians(dst_loc[0]))
    dlon = math.radians(math.radians(sta_loc[1]) - math.radians(dst_loc[1]))
    a = ((math.sin(dlat/2)) ** 2) + math.cos(math.radians(sta_loc[0])) * math.cos(math.radians(dst_loc[0])) * (math.sin(dlon/2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = constants.R * c
    return d


  def print(self):
    super().print()
    print('Neighbors: ', end='')
    print(self.neighbors)
    print('Distance: ' + str(self.edge_dist_tt))

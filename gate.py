import numpy as np
from station import Station

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
    self.gate_id = gate_id
    self.task_matrix = task_matrix
    self.day = day
    self.neighbors = neighbors
    self.edge_dist_tt = edge_dist_tt
    self.comments = comments

  # def abs_loc(self):

  def find_neighbors(self):
    pass
  def calc_edge_dist_tt(self):
    pass

  def print(self):
    super().print()

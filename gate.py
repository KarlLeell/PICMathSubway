import numpy as np
from station import Station

class Gate(Station):
  def __init__(self):
    # inherited attribute
    # self.id = ''
    # self.loc = [0, 0]
    # self.boro = ''
    # self.routes = []
    self.gate_id = ''
    self.task_matrix = np.zeors((24*12, 7))
    self.neighbors = []
    self.edge_dist_tt = []
    self.comments = ''
    # def abs_loc(self):
    #   pass
  def find_neighbors(self):
    pass
  def calc_edge_dist_tt(self):
    pass

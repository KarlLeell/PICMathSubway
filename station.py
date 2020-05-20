#==========================================
# Title:  Station Class
# Author: NYUPICMathSubwayGroup
# Date:   2020.02.24
# Comment:
#==========================================

import copy as cp

class Station:

  def __init__(self, name = '', booth_id = '', loc = None, boro = '', routes = None):
    # station name
    self.name = name
    # station booth id
    self.booth_id = booth_id
    # location of the staion in terms of geographic coordinate system, [longitude, latitude]
    self.loc = loc if loc is not None else [0, 0]
    # district: M = Manhattan, Q = Queens, BK = Brooklyn
    self.boro = boro
    # routes of subways in this station
    self.routes = routes if routes is not None else []

  # return the location
  def abs_loc(self):
    if self.loc != []:
      return [float(i) for i in self.loc]
    else:
      return [0,0]

  # update station info
  def set_station(self, name = '', booth_id = '', loc = [0,0], boro = '', routes = []):
    self.name = name
    self.booth_id = booth_id
    self.loc = cp.deepcopy(loc)
    self.boro = boro
    self.routes = cp.deepcopy(routes)

  # print the station info
  def print(self):
    print('Station Name: ' + self.name) 
    print('Station Booth ID: ' + self.booth_id) 
    print('Station Location: ' + str(self.loc))
    print('Station Boro: ' + self.boro)
    print('Station Routes: ' + str(self.routes))


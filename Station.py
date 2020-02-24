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


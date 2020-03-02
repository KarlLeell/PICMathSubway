#==========================================
# Title:  Station Class
# Author: NYUPICMathSubwayGroup
# Date:   2020.02.24
# Comment:
#==========================================

class Station:

  def __init__(self, name = '', loc = [0,0], boro = '', routes = []):
    # station name
    self.name = name
    # location of the staion in terms of geographic coordinate system, [longitude, latitude]
    self.loc = loc
    # district: M = Manhattan, Q = Queens, BK = Brooklyn
    self.boro = boro
    # routes of subways in this station
    self.routes = routes

  # return the location
  def abs_loc(self):
    return self.loc

  # update station info
  def set_station(self, name = '', loc = [0,0], boro = '', routes = []):
    self.name = name
    self.loc = loc
    self.boro = boro
    self.routes = routes

  # print the station info
  def print(self):
    print('Station Name: ' + self.name) 
    print('Station Location: ' + str(self.loc))
    print('Station Boro: ' + self.boro)
    print('Station Routes: ' + str(self.routes))


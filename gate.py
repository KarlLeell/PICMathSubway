#==========================================
# Title:  Gate Class
# Author: NYUPICMathSubwayGroup
# Date:   2020.03.02
# Comment:
# Date:   2020.03.23
#==========================================

import numpy as np
from station import Station
import math
import constants
import subprocess
import json

class Gate(Station):


  def __repr__(self):
    return self.name
  def __str__(self):
    return self.name


  def __init__(self, name = '', loc = None, boro = '', routes = None, gate_id = '', begin_time = 0,
                task_matrix = np.zeros((24*12, 1)), day = '', neighbors = None, edge_dist_tt = None, dist_prio = None,
                comments = '', value = 0, availability_priority = 0):

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
    self.dist_prio = dist_prio if dist_prio is not None else []
    self.comments = comments
    self.availability_priority = availability_priority
    self.finished = False
    self.value = value



  # def abs_loc(self):

  def find_neighbors(self):
    return self.neighbors

  def calc_travel_time(self, dst_gate):
    # if the same location return 0
    if self.loc == dst_gate.loc:
      return 0

    str1 = """ 'http://localhost:8080/otp/routers/default/plan?fromPlace="""
    str2 = """&toPlace="""
    str3 = """&time=1:02pm&date=3-18-2020&mode=TRANSIT,WALK&maxWalkDistance=500&arriveBy=false'"""
    loc1 = str(self.loc)[1:-1].replace(' ', '')
    loc2 = str(dst_gate.loc)[1:-1].replace (' ', '')
    str4 = str1 + loc1 + str2 + loc2 + str3
    travel_time = "curl" + str4
    process = subprocess.run(travel_time, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    output = process.stdout.decode('utf8')
    plans = json.loads(output)
    plan = plans.get('plan')
    if plan:
      distance = float(plan['itineraries'][0]['duration']) / 60
    else:
      if self.calc_abs_dist(dst_gate) < 0.5:
        distance = 10
      else:
        distance = 50
    return distance

  def calc_abs_dist(self, dst_gate):
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
    print('Distance Priority: ' + str(self.dist_prio))
    print('Availability Priority: ' + str(self.availability_priority))

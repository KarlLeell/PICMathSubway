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


  def __init__(self, name = '', sample_id = '', loc = None, boro = '', routes = None,
                booth_id = '', begin_time = 0, day = '', neighbors = None,
                edge_dist_tt = None, dist_prio = None, comments = '', dummy_value = 0,
                availability_priority_holder = 0, availability_priority = 0,
                task_type = constants.TASK_TYPE[0]):

    # inherited attribute
    #self.name_ = name
    #self.booth_id = booth_id
    #self.loc_ = loc
    #self.boro_ = boro
    #self.routes_ = routes
    super().__init__(name, booth_id, loc, boro, routes)
    # self attributes
    self.sample_id = sample_id
    self.begin_time = begin_time
    self.day = day
    self.neighbors = neighbors if neighbors is not None else []
    self.edge_dist_tt = edge_dist_tt if edge_dist_tt is not None else []
    self.dist_prio = dist_prio if dist_prio is not None else []
    self.comments = comments
    self.availability_priority_holder = availability_priority_holder
    self.availability_priority = availability_priority
    self.finished = False
    self.dummy_value = dummy_value
    self.task_type = task_type



  # def abs_loc(self):

  def find_neighbors(self):
    return self.neighbors

  def calc_travel_time(self, dst_gate):
    # if the same location return 0
    if self.loc == dst_gate.loc:
      return 0

    dist = None
    if self.day == constants.DAY[0]:
      total = 0
      for i in range(5):
        date = constants.DATE[i]
        dist = self.extract_travel_time(dst_gate, date)
        total = total + dist
      dist = total / 5
    elif self.day == constants.DAY[1]:
      date = constants.DATE[5]
      dist = self.extract_travel_time(dst_gate, date)
    elif self.day == constants.DAY[2]:
      date = constants.DATE[6]
      dist = self.extract_travel_time(dst_gate, date)
    if not dist:
      self.print()
    return dist

  def extract_travel_time(self, dst_gate, date):
    str1 = """ 'http://localhost:8080/otp/routers/default/plan?fromPlace="""
    str2 = """&toPlace="""
    str3 = """&time="""
    # x:xam/pm
    am_pm = 'am' if (self.begin_time + 1) % 24 < 12 else 'pm'
    time_hour = ((self.begin_time + 1) % 12)
    if 'Skip_' in self.name:
      time_hour = self.begin_time % 12
      am_pm = 'am' if self.begin_time % 24 < 12 else 'pm'
    time = str(time_hour) + ":00" + am_pm
    str4 = """&date="""
    str5 = """&mode=TRANSIT,WALK&maxWalkDistance=500&arriveBy=false'"""
    loc1 = str(self.loc)[1:-1].replace(' ', '')
    loc2 = str(dst_gate.loc)[1:-1].replace (' ', '')
    str6 = str1 + loc1 + str2 + loc2 + str3 + time + str4 + date + str5
    request = "curl" + str6

    process = subprocess.run(request, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    output = process.stdout.decode('utf8')
    plans = json.loads(output)
    plan = plans.get('plan')
    if plan:
      distance = float(plan['itineraries'][0]['duration']) / 60
    else:
      if self.calc_abs_dist(dst_gate) < 0.25:
        distance = 10
      else:
        distance = 100
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

  def print_station(self):
    super().print()

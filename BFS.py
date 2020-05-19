
import random, os, sys, time, math, argparse, subprocess, json, pickle, copy
import copy as cp
import numpy as np
from operator import attrgetter
import pandas as pd
from queue import Queue
from scipy import stats
from tqdm import tqdm
import constants
from DaySchedule import DaySchedule
from WeekSchedule import WeekSchedule
from gate import Gate
import read_tasks as read_tasks
import read_checkers as read_checkers
import performance_measure as performance_measure

import xlwt 
from xlwt import Workbook 

class Params:
  def __init__(self, checker_shift_start, full_time = True, weights=[], sp=0.01, lapse_rate=0, pruning_threshold=float('inf'), mu=0.0, sigma=1.0):
    self.checker_shift_start = checker_shift_start
    if full_time:
      self.checker_shift_end = checker_shift_start + 7
    else:
      self.checker_shift_end = checker_shift_start + 6
    self.full_time = full_time
    self.weights = weights
    self.stopping_probability = sp
    self.lapse_rate = lapse_rate
    self.pruning_threshold = pruning_threshold
    self.mu = mu
    self.sigma = sigma
  
class Node(Gate):
  def __init__(self, gate):
    self.gate = gate
    self.parent = None
    self.children = []
    self.availability_priority = self.gate.availability_priority
    self.dist_priority_list = self.gate.dist_prio
    self.cumm_delay = 0
    self.value = 0
    self.terminate = False
  def calc_dist_priority(self, child_idx):
    return self.dist_priority_list[child_idx]
  def remove_child(self, n):
    pass
  def heuristic_value(self, parent_node, idx):
    self.value = parent_node.calc_dist_priority(idx) + self.availability_priority
    if ('Skip' not in self.gate.name) and ('LIC' not in self.gate.name):
      self.value += 1
    return self.value


def Lapse(probability):
  ''' return true with a certain probability '''
  return random.random() < probability

def Stop(probability):
  ''' return true with a certain probability '''
  return random.random() < probability

# def RandomMove(node, params):
#   ''' make a random move '''
#   InitializeChildren(node, params)
#   return random.choice(node.children)

def InitializeChildren(node, cumm_delay, params):
  if verbose:
    print('InitializeChildren')
    print("\tAdd children to node "+str(node.gate.name))
    print('\tNeighbors(candidates): '+str(node.gate.neighbors))
  if params.full_time and node.gate.begin_time == (params.checker_shift_start + 1)%24: # default 30-minute lunch break starts at the third hour 
    if verbose:
      print('lunch break at hour '+str(params.checker_shift_start + 2))
    for i in range(len(node.gate.neighbors)):
      if 'Skip' in node.gate.neighbors[i].name:
        child = Node(node.gate.neighbors[i]) # add the skipping node as the lunck break node
    child.parent = node
    child.heuristic_value(node, 1)
    # child.value = node.calc_dist_priority(i) + child.availability_priority
    node.children.append(child)
    return node.children
  # print(node.gate.name)
  for i in range(1,len(node.gate.neighbors)): # normal hour, ignore the LIC node
    if verbose:
      print('\n\t\tConsidering node '+str(node.gate.neighbors[i].name))
    if('Skip' in node.gate.name or 'LIC' in node.gate.name):
      duration = 0 # if current node is skip node, task duration is 0 (1-hour available travel time)
      if(params.full_time and node.gate.begin_time == (params.checker_shift_start+2)%24):
        duration = 0.5 # after lunch break, only look at children 30 minutes away
    else:
      duration = 1 # if current node is real task, task duration is 1 hour
    if verbose:
      print('\t\tnode.gate.neighbors[i].begin_time + 0.2 = '+str(node.gate.neighbors[i].begin_time + 0.2))
      print('\t\tnode.gate.begin_time + duration + node.gate.edge_dist_tt[i]/60.0 = '+str((node.gate.begin_time + duration) + node.gate.edge_dist_tt[i]/60.0))
    if node.gate.begin_time == 23: # overnight task
      duration -= 24 # -23 for a real task, -24 for skip node
    
    # if 'Skip' in node.gate.neighbors[i].name :
    #   print(node.gate.neighbors[i].name)
    #   print('\t\tnode.gate.neighbors[i].begin_time + 0.2 = '+str(node.gate.neighbors[i].begin_time + 0.2))
    #   print('\t\tnode.gate.begin_time + duration + node.gate.edge_dist_tt[i]/60.0 = '+str((node.gate.begin_time + duration) + node.gate.edge_dist_tt[i]/60.0))
    if (node.gate.neighbors[i].begin_time + 0.2 >= (node.gate.begin_time + duration) + node.gate.edge_dist_tt[i]/60.0 and cumm_delay/60.0 + node.gate.edge_dist_tt[i]/60.0 <= .5):
      # if viable in terms of start time and 12 minutes delay
      if verbose:
        print('\t\t\tviable in terms of start time')
      # if 'Skip' in node.gate.neighbors[i].name:
      #   print('\t\t\tviable in terms of start time')
      if(CheckLicDist(node.gate.neighbors[i], cumm_delay, params)):
        # if can return to LIC on time
        if verbose:
          print('\t\t\tviable to return to LIC')
        # if 'Skip' in node.gate.neighbors[i].name:
        #   print('\t\t\tviable to return to LIC')
        child = Node(node.gate.neighbors[i])
        child.parent = node
        child.heuristic_value(node, i)
        # child.value = node.calc_dist_priority(i) + child.availability_priority
        node.children.append(child)
        if verbose:
          print("\t\t\tadd child "+str(child.gate.name) +", value "+str(child.value))
          print('\t\tnode dist_prio='+str(node.calc_dist_priority(i))+', avail_prio='+str(child.availability_priority))
        # if 'Skip' in node.gate.neighbors[i].name:
        #   print("\t\t\tadd child "+str(child.gate.name) +", value "+str(child.value))
        #   print('\t\tnode dist_prio='+str(node.calc_dist_priority(i))+', avail_prio='+str(child.availability_priority))
  if(CheckLicDist(node.gate, cumm_delay, params, 1) == False):
    if verbose:
      print('\tcurrent node is terminal, no children expanded: '+str(node.gate.name))
      node.children = []
      node.terminate = True

  return node.children

def CheckLicDist(gate, cumm_delay, params, extra_time = 0):
  if verbose:
    print('Inside CheckLicDist')
    gate.print()
    print(gate.name + " edge dist: " +  str(gate.edge_dist_tt[0]))
  if gate.begin_time < 8:
    result = params.checker_shift_end%24 - (gate.begin_time + 1 + extra_time + gate.edge_dist_tt[0]/60.0 + cumm_delay/60.0)
  else:
    result = params.checker_shift_end - (gate.begin_time + 1 + extra_time + gate.edge_dist_tt[0]/60.0 + cumm_delay/60.0)
  if verbose:
    print(result)
  return result >= 0

def SelectNode(root):
  cumm_delay = 0
  ''' return the leaf node along the most promising branch '''
  n = root
  if verbose:
    print('SelectNode')
    print('\troot='+str(n.gate.name))
  prev_task = root
  while len(n.children) != 0:
    n = ArgmaxChild(n)
    if ("Skip" not in prev_task.gate.name and "LIC" not in prev_task.gate.name) and ("Skip" not in n.gate.name and "LIC" not in n.gate.name):
      for i in range(len(prev_task.gate.neighbors)):
        if(n.gate == prev_task.gate.neighbors[i]):
          cumm_delay += prev_task.gate.edge_dist_tt[i]
    if verbose:
      print('\targmaxchild '+str(n.gate.name))
      print('\tdelay '+str(cumm_delay))
    prev_task = n
  if verbose:
    print('\texits selectnode while')
  if(cumm_delay%6 != 0):
    cumm_delay = (int(cumm_delay/6) + 1) * 6
  n.cumm_delay = cumm_delay
  return n, cumm_delay

def ExpandNode(node, cumm_delay, params):
  ''' expand the current node with children, prune '''
  if verbose:
    print('ExpandNode: '+str(node.gate.name))
  InitializeChildren(node, cumm_delay, params)
  if node.terminate:
    return
  Vmaxchild = ArgmaxChild(node)
  if verbose:
    print("\tVmaxchild " + str(Vmaxchild.gate.name)+" with value "+str(Vmaxchild.value))
  Vmax = Vmaxchild.value
  for n in node.children:
      if abs(n.value - Vmax) > params.pruning_threshold:
        if verbose:
          print('remove_child because larger than threshold')
        n.remove_child(n)

def Backpropagate(node, root, value):
  ''' update value back until root node '''
  if verbose:
    print('Backpropagate: current node '+str(node.gate.name))
  if not node.terminate:
    node.value = value
  if node != root:
    Backpropagate(node.parent, root, value)

def PathAverage(node, root, pathsum, counter): #exclude root value from pathsum
  if node != root:
    pathsum += node.value
    counter += 1.0
    return PathAverage(node.parent, root, pathsum, counter)
  return pathsum/counter

def ArgmaxChild(node):
  ''' return the child with max value '''
  if verbose: 
    print('ArgmaxChild '+str(node.gate.name))
    if len(node.children) == 0:
      print(node.gate.name + " " + str(node.gate.neighbors))
      graphs[0].print()
  maxchild = node.children[0]
  for i in range(len(node.children)):
    if node.children[i].value >= maxchild.value:
      maxchild = node.children[i]
    if verbose:
      print('\tchild value: '+str(node.children[i].value))
  maxvalue = maxchild.value 
  if verbose:
    print('\tmaxchild value: '+str(maxvalue))
  # randomly choose one if have multiple max values
  return random.choice([i for i in node.children if i.value == maxvalue])

def MakeMove(root, params):
  ''' make an optimal move according to value function '''
  if verbose:
    print("MakeMove root.value " +str(root.value))
  assert len(root.children) == 0
  # if Lapse(params.lapse_rate):
  #   if verbose:
  #     print("random move")
  #   return RandomMove(root, params)
  # else:
  terminal_found = False
  while not (Stop(params.stopping_probability) and terminal_found):
    if verbose:
      print("enter loop")
    leaf, cumm_delay = SelectNode(root)
    if verbose:
      print('selected node '+str(leaf.gate.name))
    if leaf.terminate:
      terminal_found = True
      continue
    ExpandNode(leaf, cumm_delay, params)
    if leaf.terminate:
      terminal_found = True
      if verbose:
        print("terminal node encountered")
      continue
    pathavg = PathAverage(ArgmaxChild(leaf), root, 0, 0)
    if verbose:
      print('PathAverage: '+str(pathavg))
    Backpropagate(ArgmaxChild(leaf), root, pathavg)
    if verbose:
      print('root value after backprop '+str(root.value))
    if root.children == []:
      ExpandNode(root, cumm_delay,params)
      if verbose:
        print("doesn't enter loop")
  if verbose:
    print("make decision")
  return ArgmaxChild(root)

def print_decision_path(node, root, verbose=False):
  n = node
  nodes = [node]
  delay_array = [0,0]
  travel_time_array = [0]
  for i in range(len(root.gate.neighbors)):
        if(n.gate == root.gate.neighbors[i]):
          travel_time_array.append(root.gate.edge_dist_tt[i])
  if verbose:
    print('---- start print_decision_path')
    print('travel from LIC')
    print(str(n.gate.name))
  prev_task = node
  cumm_delay = 0
  while len(n.children) != 0:
    n = ArgmaxChild(n)
    nodes.append(n)
    delay_array.append(n.cumm_delay)
    if ("Skip" not in prev_task.gate.name and "LIC" not in prev_task.gate.name) and ("Skip" not in n.gate.name and "LIC" not in n.gate.name):
      for i in range(len(prev_task.gate.neighbors)):
        if(n.gate == prev_task.gate.neighbors[i]):
          cumm_delay += prev_task.gate.edge_dist_tt[i]
          if verbose:
            print("distance to: " + str(prev_task.gate.edge_dist_tt[i]))     
    for i in range(len(prev_task.gate.neighbors)):
        if(n.gate == prev_task.gate.neighbors[i]):
          travel_time_array.append(prev_task.gate.edge_dist_tt[i])
    if(cumm_delay%6 != 0):
      cumm_delay = (int(cumm_delay/6) + 1) * 6
    if verbose:
      print("delay: " + str(cumm_delay))
      print("node delay: " + str(n.cumm_delay))
      print("travel time: " + str(travel_time_array[-1]))
      print(str(n.gate.name))
    prev_task = n
  delay_array.append(cumm_delay)
  travel_time_array.append(n.gate.edge_dist_tt[0])
  if verbose:
    print('return to LIC')
    print('delays: ' + str(delay_array))
    print('travel times: ' + str(travel_time_array))
    print('---- end print_decision_path')

  return nodes, delay_array, travel_time_array

def make_gate_array(root):
  gate_array = []
  n = root
  gate_array.append(n.gate) # first node travel from LIC
  while len(n.children) != 0:
    n = ArgmaxChild(n)
    gate_array.append(n.gate)
  gate_array.append(n.gate.neighbors[0]) # last node travel back to LIC
  return gate_array

def get_value(node):
  n = node
  value = n.value
  while len(n.children) != 0:
    n = ArgmaxChild(n)
    value += n.value
  return value

def delete_nodes(nodes, graph, verbose=False):
  while len(nodes) > 0:
    gate = nodes.pop().gate
    if verbose:
      print("Considering deleting node " + gate.name)
    if("Skip" not in gate.name and "LIC" not in gate.name):
      if verbose:
        print(gate.begin_time)
      status = graph.delete_vertex(booth_id = gate.booth_id, begin_time = gate.begin_time)
      if verbose:
        print('status '+str(status))
  return graph

def week_bfs_for1(graphs, checker): # create schedule for a week (one checker)
  checker.print()
  duration = 0
  if checker.ft_work_status:
    duration = 7
  else:
    duration = 6
  week_values = []

  for start_time in range(checker.shift_start, checker.shift_start+13-duration+1):
    wkd_graph = copy.deepcopy(graphs[0])
    sat_graph = copy.deepcopy(graphs[1])
    sun_graph = copy.deepcopy(graphs[2])
    week_value = 0
    params = Params(start_time, full_time = checker.ft_work_status)
    for day in checker.working_days:
      if day in [1,2,3,4,5]:
        gates = wkd_graph
      elif day == 6:
        gates = sat_graph
      else:
        gates = sun_graph
      root = Node(gates.vertices[start_time][0]) # choose the lic node as root node
      decision_node = MakeMove(root, params)
      nodes_path, _, _ = print_decision_path(decision_node, root)
      path_value = get_value(decision_node)
      week_value += path_value
      if day in [1,2,3,4,5]:
        wkd_graph = delete_nodes(nodes_path, gates)
      elif day == 6:
        sat_graph = delete_nodes(nodes_path, gates)
      else:
        sun_graph = delete_nodes(nodes_path, gates)
    week_values.append(week_value)
  # print("for checker " + checker.name + ": " + str(week_values))


  #find best shift start time for each day
  best_shift_start = range(checker.shift_start, checker.shift_start+13-duration+1)[week_values.index(max(week_values))]
  if best_shift_start == checker.shift_start:
    start_range = [best_shift_start, (best_shift_start+1+24)%24,(best_shift_start+2+24)%24]
  elif best_shift_start == checker.shift_start+13-duration:
    start_range = [(best_shift_start-2+24)%24, (best_shift_start-1+24)%24, best_shift_start]
  else:
    start_range = [(best_shift_start-1+24)%24, best_shift_start, (best_shift_start+1+24)%24]

  ds_array = [] # day schedule array for the week
  for day in checker.working_days:
    day_values = []
    day_value = 0
    for start_time in start_range:
      wkd_graph = copy.deepcopy(graphs[0])
      sat_graph = copy.deepcopy(graphs[1])
      sun_graph = copy.deepcopy(graphs[2])
      params = Params(start_time, full_time = checker.ft_work_status)

      if day in [1,2,3,4,5]:
        gates = wkd_graph
      elif day == 6:
        gates = sat_graph
      else:
        gates = sun_graph
      root = Node(gates.vertices[start_time][0]) # choose the lic node as root node
      decision_node = MakeMove(root, params)
      nodes_path, _, _ = print_decision_path(decision_node, root)
      day_value = get_value(decision_node)
      if day in [1,2,3,4,5]:
        wkd_graph = delete_nodes(nodes_path, gates)
      elif day == 6:
        sat_graph = delete_nodes(nodes_path, gates)
      else:
        sun_graph = delete_nodes(nodes_path, gates)
      day_values.append(day_value)

    # run again using best shift start for each day
    print('---- best shift start: '+str(best_shift_start))
    # run week schedule again using best shift start time
    wkd_graph = graphs[0] # edit the original graphs
    sat_graph = graphs[1] 
    sun_graph = graphs[2]
    
    start_time = start_range[day_values.index(max(day_values))]
    params = Params(start_time, full_time = checker.ft_work_status)
    if day in [1,2,3,4,5]:
      gates = wkd_graph
    elif day == 6:
      gates = sat_graph
    else:
      gates = sun_graph
    root = Node(gates.vertices[start_time][0]) # choose the lic node as root node
    decision_node = MakeMove(root, params)
    nodes_path, delay_array, travel_time_array = print_decision_path(decision_node, root, True)
    if day in [1,2,3,4,5]:
      wkd_graph = delete_nodes(nodes_path, gates)
    elif day == 6:
      sat_graph = delete_nodes(nodes_path, gates)
    else:
      sun_graph = delete_nodes(nodes_path, gates)
  
    ds = DaySchedule(checker, day, start_time, start_time+duration, make_gate_array(root), delay_array, travel_time_array)
    ds_array.append(ds)

  print('\n\n---------------- return')
  # return updated graphs after running with best shift start for a week
  return [wkd_graph, sat_graph, sun_graph], WeekSchedule(checker, start_time, start_time+duration, ds_array,)

def week_bfs_forall(graphs, checkers, random_throw = False, throw_probability = .8): # create schedule for a week (all checkers)
  wks_forall = []
  failed_tasks = []
  for count,checker in enumerate(random.sample(checkers, len(checkers))):
    if count % 5 == 0:
      graphs[0].add_special_sample()
    graphs, wks = week_bfs_for1(graphs, checker)
    if random_throw and random.random() < throw_probability:
      for task in random.choice(wks.DaySchedule_array).gate_array:
        # if('Skip' not in task.name and 'LIC' not in task.name and task.task_type != 'S'):
        if('Skip' not in task.name and 'LIC' not in task.name):
          failed_tasks.append(task)
    wks_forall.append(wks)
  return wks_forall, graphs, failed_tasks

def failed_tasks_to_excel_1(failed_tasks):
  task_dict = {'sample_id': [], 'booth_id': [],'loc': [], 'day': [], 'begin': [], 'end': [], 'sta': [], 'boro': [], 'routes': [], 'staname': [], 'gate_signage': [], 'comments_for_checker': []}
  for task in failed_tasks:
    task_dict['sample_id'].append(task.sample_id)
    task_dict['booth_id'].append(task.booth_id)
    task_dict['loc'].append(task.loc)
    task_dict['day'].append(task.day)
    task_dict['begin'].append((task.begin_time) * 100)
    task_dict['end'].append((task.begin_time) * 100 + 100)
    task_dict['sta'].append(task.name)
    task_dict['boro'].append(task.boro)
    task_dict['routes'].append(','.join(task.routes))
    task_dict['staname'].append(task.name)
    task_dict['gate_signage'].append("")
    task_dict['comments_for_checker'].append(task.comments)

  df = pd.DataFrame.from_dict(task_dict)
  df.to_excel("failed_tasks_1.xlsx", index=False)
  return "failed_tasks_1.xlsx"

def failed_tasks_to_excel_2(failed_tasks):
  task_dict = {'sample_id': [], 'booth_id': [],'loc': [], 'day': [], 'begin': [], 'end': [], 'sta': [], 'boro': [], 'routes': [], 'staname': [], 'gate_signage': [], 'comments_for_checker': []}
  for task in failed_tasks:
    task_dict['sample_id'].append(task.sample_id)
    task_dict['booth_id'].append(task.booth_id)
    task_dict['loc'].append(task.loc)
    task_dict['day'].append(task.day)
    task_dict['begin'].append((task.begin_time) * 100)
    task_dict['end'].append((task.begin_time) * 100 + 100)
    task_dict['sta'].append(task.name)
    task_dict['boro'].append(task.boro)
    task_dict['routes'].append(','.join(task.routes))
    task_dict['staname'].append(task.name)
    task_dict['gate_signage'].append("")
    task_dict['comments_for_checker'].append(task.comments)

  df = pd.DataFrame.from_dict(task_dict)
  df.to_excel("failed_tasks_2.xlsx", index=False)
  return "failed_tasks_2.xlsx"

def month_bfs_forall(graphs, checkers): # create schedule for a week (all checkers)
  month_forall = []
  failed_tasks_month = []
  for week in range(4):
    if(week == 2):
      print("before 2:\n")
      graphs[0].print()
      graphs[1].print()
      graphs[2].print()
      path = "./" + failed_tasks_to_excel_1(failed_tasks_month[week-2])
      read_tasks.read_failed_tasks(graphs, path)
      print("after 2:\n")
      graphs[0].print()
      graphs[1].print()
      graphs[2].print()
    if(week == 3):
      print("before 3:\n")
      graphs[0].print()
      graphs[1].print()
      graphs[2].print()
      path = "./" + failed_tasks_to_excel_2(failed_tasks_month[week-2])
      read_tasks.read_failed_tasks(graphs, path)
      print("after 3:\n")
      graphs[0].print()
      graphs[1].print()
      graphs[2].print()
    print('\n\n WEEK'+str(week))
    wks_forall, graphs, failed_tasks_week = week_bfs_forall(graphs, checkers, True)
    month_forall.append(wks_forall)
    failed_tasks_month.append(failed_tasks_week)
  return month_forall, failed_tasks_month

def print_schedule(month_forall, filename):
  wb = Workbook() 
  style = xlwt.easyxf('font: bold 1') 
  days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  for weekSchedule in month_forall:
    week1 = wb.add_sheet(weekSchedule.checker.name)
    i = 0
    for daySchedule, i in zip(weekSchedule.DaySchedule_array, range(len(weekSchedule.DaySchedule_array[0].gate_array))):
      week1.write(0,daySchedule.day,days[daySchedule.day-1], style);
      for task, i in zip(daySchedule.gate_array, range(len(daySchedule.gate_array))):
        if(i == len(daySchedule.gate_array)-1):
          time1 = time2
          time2 = str((daySchedule.shift_start+i+1)%24) + ":00"
        else:
          time1 = str((daySchedule.shift_start+i)%24) + ":" + str(daySchedule.delay_array[i]).zfill(2)
          time2 = str((daySchedule.shift_start+i+1)%24) + ":" + str(daySchedule.delay_array[i]).zfill(2)
        
        week1.write(i*2+1,daySchedule.day, time1 + " - " + time2, style)
        if 'Skip' in task.name or 'LIC' in task.name:
          if daySchedule.checker.ft_work_status == True and i == 2:
            week1.write(i*2+2,daySchedule.day,"lunch break")
          else:
            week1.write(i*2+2,daySchedule.day,"traveling")
        else:
          week1.write(i*2+2,daySchedule.day,task.name)
  wb.save('xlwt ' + filename) 

verbose = False
checkers = read_checkers.read_checkers('NYCT FE Required Data/FE Checker list ASSIGNED.xlsx')
wkd_save = pickle.load(open('wkd_save.pkl', 'rb'))
sat_save = pickle.load(open('sat_save.pkl', 'rb'))
sun_save = pickle.load(open('sun_save.pkl', 'rb'))
graphs = [wkd_save, sat_save, sun_save]

month_forall, failed_tasks_month = month_bfs_forall(graphs, checkers)

graphs[0].print()
graphs[1].print()
graphs[2].print()

print_schedule(month_forall[0], 'week1.xls')
print_schedule(month_forall[1], 'week2.xls')
print_schedule(month_forall[2], 'week3.xls')
print_schedule(month_forall[3], 'week4.xls')

dbfile = open('./month_forall.pickle', 'ab')
pickle.dump(month_forall, dbfile)

performance_measure.completion(145,158)
performance_measure.efficiency()


# try:
#   month_forall, failed_tasks_month = month_bfs_forall(graphs, checkers)

#   graphs[0].print()
#   graphs[1].print()
#   graphs[2].print()

#   print_schedule(month_forall[0], 'week1.xls')
#   print_schedule(month_forall[1], 'week2.xls')
#   print_schedule(month_forall[2], 'week3.xls')
#   print_schedule(month_forall[3], 'week4.xls')

#   dbfile = open('./month_forall.pickle', 'ab')
#   pickle.dump(month_forall, dbfile)

#   performance_measure.completion(145,158)
#   performance_measure.efficiency()

# except:
#   graphs[0].print()
#   graphs[1].print()
#   graphs[2].print()

#   wkd = open('wkd_save_error.pickle', 'wb')
#   pickle.dump(graphs[0], wkd)
#   sat = open('sat_save_error.pickle', 'wb')
#   pickle.dump(graphs[1], sat)
#   sun = open('sun_save_error.pickle', 'wb')
#   pickle.dump(graphs[2], sun)

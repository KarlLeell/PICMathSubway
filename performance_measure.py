import random, os, sys, time, math, argparse, subprocess, json, pickle, copy
import copy as cp
import numpy as np
from operator import attrgetter
import pandas as pd
from queue import Queue
from scipy import stats
from tqdm import tqdm
import constants

def efficiency():
  dbfile = open('./month_forall.pickle', 'rb')      
  MonthSchedule = pickle.load(dbfile)
  time_working = 0
  time_checking = 0
  for week in MonthSchedule:
    for WeekSchedule in week:
      for DaySchedule in WeekSchedule.DaySchedule_array:
        shift_start = DaySchedule.shift_start
        shift_end = DaySchedule.shift_end
        if shift_start < shift_end:
          time_working += shift_end - shift_start
        elif shift_start > shift_end:
          time_working += 24 - shift_start + shift_end
        for task in DaySchedule.gate_array:
          if 'Skip' not in task.name and 'LIC' not in task.name:
            time_checking += 1
  print('total checking hours:', time_checking)
  print('total working hours:', time_working)
  print('working efficiency:', time_checking/time_working)


def completion(total_tasks, total_special_tasks):
  dbfile = open('./month_forall.pickle', 'rb')      
  MonthSchedule = pickle.load(dbfile)
  sheet1 = pd.read_excel('./failed_tasks_1.xlsx')
  sheet2 = pd.read_excel('./failed_tasks_2.xlsx')
  rescheduled_tasks = len(sheet1) + len(sheet2)
  completed_tasks = 0
  completed_special_tasks = 0
  completed_rescheduled_tasks = 0
  for week in MonthSchedule:
    for WeekSchedule in week:
      for DaySchedule in WeekSchedule.DaySchedule_array:
        for task in DaySchedule.gate_array:
          if 'Skip' not in task.name and 'LIC' not in task.name:
            if task.task_type == 'N':
              completed_tasks += 1
            elif task.task_type == 'S':
              completed_special_tasks += 1
            else:
              completed_rescheduled_tasks += 1

  print('base tasks completed:', completed_tasks + completed_rescheduled_tasks-rescheduled_tasks, 'out of', total_tasks)
  print('proportion of base sample completed:', (completed_tasks + completed_rescheduled_tasks-rescheduled_tasks)/total_tasks)
  print('rescheduled tasks completed:', completed_rescheduled_tasks, 'out of', rescheduled_tasks)
  print('proportion of rescheduled tasks  completed:', completed_rescheduled_tasks/rescheduled_tasks)
  print('special tasks completed:', completed_special_tasks, 'out of', total_special_tasks)
  print('proportion of special sample completed:', completed_special_tasks/total_special_tasks)

completion(145, 158)
efficiency()

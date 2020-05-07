def efficiency(MonthSchedule):
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
  return(time_checking/time_working)



def completion(MonthSchedule,total_tasks):
  completed_tasks = 0
  for week in MonthSchedule:
    for WeekSchedule in week:
      for DaySchedule in WeekSchedule.DaySchedule_array:
        for task in DaySchedule.gate_array:
          if 'Skip' not in task.name and 'LIC' not in task.name:
            completed_tasks += 1
  print('base tasks completed:', completed_tasks, 'out of', total_tasks)
  print('proportion of base sample completed:', completed_tasks/total_tasks)
  return(completed_tasks/total_tasks)



def completion_special(MonthSchedule,total_special_tasks):
  completed_special_tasks = 0
  for week in MonthSchedule:
    for WeekSchedule in week:
      for DaySchedule in WeekSchedule.DaySchedule_array:
        for task in DaySchedule.gate_array:
          if task.task_type == 'S':
            completed_special_tasks += 1
  print('special tasks completed:', completed_special_tasks, 'out of', total_special_tasks)
  print('proportion of special sample completed:', completed_special_tasks/total_special_tasks)
  return(completed_special_tasks/total_special_tasks)


        

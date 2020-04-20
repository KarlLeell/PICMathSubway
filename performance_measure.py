def effeciency_check(MonthSchedule):
  time_working = 0
  time_checking = 0
  for WeekSchedule in MonthSchedule:
    for DaySchedule in WeekSchedule.DaySchedule_array:
      shift_start = DaySchedule.shift_start
      shift_end = DaySchedule.shift_end
      if shift_start < shift_end:
        time_working += shift_start - shift_end
      elif shift_start > shift_end:
        time_working += 24 - shift_start + shift_end
      for task in DaySchedule.gate_array:
        time_checking += 1
  return(time_checking/time_working)

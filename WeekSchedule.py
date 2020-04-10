class WeekSchedule:
# schedule for one checker for a week (array of DaySchedule objects)
  def __init__(self, checker, shift_start, shift_end, DaySchedule_array):
    self.checker = checker
    self.shift_start = shift_start
    self.shift_end = shift_end
    self.DaySchedule_array = DaySchedule_array
    self.days = self.checker.working_days
    self.rdo = self.checker.rdo
  def print(self):
    for ds in self.DaySchedule_array:
      print('WeekSchedule for checker '+str(self.checker.name))
      ds.print()
class DaySchedule:
# schedule for one checker for a day
  def __init__(self, checker, day, shift_start, shift_end, gate_array, delay_array):
    self.checker = checker
    self.day = day
    self.shift_start = shift_start
    self.shift_end = shift_end % 24
    self.gate_array = gate_array # array of gate objects
    self.delay_array = delay_array
    # assert len(gate_array) == shift_end - shift_start
  def print(self):
    print('DaySchedule: day '+str(self.day)+' for checker '+str(self.checker.name))
    print('\tshift '+str(self.shift_start)+' to '+str(self.shift_end))
    for task, i in zip(self.gate_array, range(len(self.gate_array))):
      print('\ttime '+str((self.shift_start+i+self.delay_array[i]/60.0)%24))
      if 'Skip' in task.name or 'LIC' in task.name:
        print('\ttraveling')
      # print(task.print()) ########## need to fix this
      else:
        print('\t'+str(task.name))
        # print(task.print())
class Checker:
  def __init__(self, name, shift_start, shift_end, ft_work_status, rdo, working_days):
    self.name = name
    self.ft_work_status = ft_work_status
    self.shift_start = shift_start
    self.shift_end = shift_end
    self.rdo = rdo
    self.working_days = working_days

  def print(self):
    print('Name: ' + self.name + ' shift start: ' + str(self.shift_start))

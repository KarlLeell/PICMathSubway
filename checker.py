import numpy as np
import pandas as pd

# filename = 'FE_Checker_List.csv'
# checkers = pd.read_csv(filename)
# checkers = checkers.loc[0:30,'checker':'rdo']

class Checker:
  def __init__(self, name, shift_start, shift_end, ft_work_status, rdo):
    self.name = name
    self.ft_work_status = ft_work_status
    self.shift_start = shift_start
    self.shift_end = shift_end
    self.avail_matrix = self.make_table(shift_start, shift_end, rdo)
    self.rdo = self.make_rdo_table(rdo)
    
  #monday - sunday
  def make_table(self, shift_start, shift_end, rdo):
    table = np.zeros((288, 7), dtype = int)
    rdo_days = rdo.split(" ");
    if(rdo_days[0] == 'FRI'):
      skip = [4,5]
    elif(rdo_days[0] == 'SAT'):
      skip = [5,6]
    else:
      skip = [0,6]
    for i in range(int(shift_start*12/100),int(shift_end*12/100)):
      for j in range(0,7):
        if(j not in skip):
          table[i][j] = 1
    return table
    
  def make_rdo_table(self, rdo):
    table = np.zeros((288, 7), dtype = int)
    rdo_days = rdo.split(" ");
    if(rdo_days[0] == 'FRI'):
      skip = [4,5]
    elif(rdo_days[0] == 'SAT'):
      skip = [5,6]
    else:
      skip = [0,6]
    for i in range(0,288):
      for j in skip:
          table[i][j] = 1
    return table
    

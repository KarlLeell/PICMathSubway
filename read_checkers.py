import numpy as np
import pandas as pd
import argparse
from checker import Checker
import constants


def read_checkers(path):
  ''' returns a list of checkers '''
  sheet = pd.read_excel(path)
  rows = 31
  checkers = []
  for i in range(19, rows):
    name = str(sheet.values[i, 0])
    shift_start = int(sheet.values[i, 2]/100)
    if(sheet.values[i, 4] == 'Full Time'):
      ft_work_status = True
      # shift_end = shift_start + 7
    else:
      ft_work_status = False
      # shift_end = shift_start + 6
    shift_end = int(sheet.values[i, 3]/100)
    rdo_str = str(sheet.values[i, 5])[:3]
    # 1 = MON
    if(rdo_str == 'FRI'):
      rdo = [5,6]
      working_days = [7,1,2,3,4]
    elif (rdo_str == 'SAT'):
      rdo = [6,7]
      working_days = [1,2,3,4,5]
    else:
      rdo = [7,1]
      working_days = [2,3,4,5,6]

    checker = Checker(name, shift_start, shift_end, ft_work_status, rdo, working_days)
    print(checker.name)
    checkers.append(checker)

  return checkers


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--file_loc', default='NYCT FE Required Data/FE Checker list.xlsx', type=str)
  args = parser.parse_args()
  path = args.file_loc
  read(path)

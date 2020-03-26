import numpy as np
import pandas as pd
import argparse
from checker import Checker
import constants


def read(path):
  # print(args.file_loc)
  sheet = pd.read_excel(path)
  rows = 31
  checkers = []
  for i in range(0, rows):
    name = str(sheet.values[i, 0])

    shift_start = int(sheet.values[i, 2]/100)

    if(sheet.values[i, 4] == 'Full Time'):
      ft_work_status = True
      shift_end = shift_start + 7
    else:
      ft_work_status = False
      shift_end = shift_start + 6
    rdo = str(sheet.values[i, 5])[:3]

    checker = Checker(name, shift_start, shift_end, ft_work_status, rdo)
    print(checker.name)
    checkers.append(checker)

  return checkers


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--file_loc', default='NYCT FE Required Data/FE_Checker list.xlsx', type=str)
  args = parser.parse_args()
  path = args.file_loc
  read(path)
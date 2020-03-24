import random, os, sys, time
import numpy as np
from operator import attrgetter
import argparse
from gate import Gate
import read_tasks as read_tasks
import read_checkers as read_checkers

class Params:
  def __init__(self, weights=[], sp=0.10, lapse_rate=0.05, pruning_threshold=0.0, mu=0.0, sigma=1.0):
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
    self.value = self.gate.value
    self.terminate = self.gate.finished
  def heuristic_value_function(self):
    pass
  def remove_child(self, n):
    pass

def Lapse(probability):
  ''' return true with a certain probability '''
  return random.random() < probability

def Stop(probability):
  ''' return true with a certain probability '''
  return random.random() < probability

def RandomMove(node, params):
  ''' make a random move '''
  InitializeChildren(node, params)
  return random.choice(node.children)

def InitializeChildren(node, params):
  print("Add children to node "+str(node.gate.name))
  for i in range(len(node.gate.neighbors)):
    if (node.gate.neighbors[i].begin_time - node.gate.edge_dist_tt[i] >= node.gate.begin_time + 1):
      child = Node(node.gate.neighbors[i])
      child.parent = node
      node.children.append(child)
      print("\tadd nonempty child "+str(child.gate.name) +"\tvalue "+str(child.value))
  return node.children

def SelectNode(root):
  ''' return the leaf node along the most promising branch '''
  n = root
  while len(n.children) != 0:
    n = ArgmaxChild(n)
  return n

def ExpandNode(node, params):
  ''' expand the current node with children, prune '''
  print('Expand node '+str(node.gate.name))
  InitializeChildren(node, params)
  Vmaxchild = ArgmaxChild(node)
  print("\tVmaxchild " + str(Vmaxchild.gate.name)+" with value "+str(Vmaxchild.value))
  Vmax = Vmaxchild.value
  for n in node.children:
      if abs(n.value - Vmax) > params.pruning_threshold:
        n.remove_child(n)

def Backpropagate(node, root):
  ''' update value back until root node '''
  node.value = ArgmaxChild(node).value
  if node != root:
    Backpropagate(node.parent, root)

def ArgmaxChild(node):
  ''' return the child with max value '''
  return max(node.children, key=attrgetter('value'))

def MakeMove(root, params):
  ''' make an optimal move according to value function '''
  print("MakeMove root.value " +str(root.value))
  assert len(root.children) == 0
  if Lapse(params.lapse_rate):
    print("random move")
    return RandomMove(root, params)
  else:
    while not Stop(params.stopping_probability):
      print("enter loop")
      leaf = SelectNode(root)
      print('Select Node '+str(leaf.gate.name))
      if leaf.terminate:
        print("terminal node encountered, break")
        break
      ExpandNode(leaf, params)
      Backpropagate(leaf, root)
      print('Root value after backprop '+str(root.value))
    if root.children == []:
      ExpandNode(root, params)
      print("doesn't enter loop")
  print("make decision")
  return ArgmaxChild(root)


def print_moves(root):
  print(root.gate.name)
  root = SelectNode(root)
  print_moves(root)

# def main(args):
if __name__ == '__main__':
  params = Params()

  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--file_loc', default='NYCT FE Required Data/SFE SAMPLE210.xlsx', type=str)
  parser.add_argument('-s', '--station_loc', default='NYCT FE Required Data/station_location.csv', type=str)
  args = parser.parse_args()
  path = [args.file_loc, args.station_loc]
  graphs = read_tasks.read(path)

  checker_path = 'NYCT FE Required Data/FE_Checker list.xlsx'
  checkers = read_checkers.read(checker_path)

  # only working with weekday tasks
  gates = graphs[0]

  gates.print()
  for checker in checkers:
    checker.print()

  current_checker = checkers[0]
  start_time = int(current_checker.shift_start/100)

  root = Node(gates.vertices[start_time][1])
  print("root: " + root.gate.name)

  print("decision: "+str(MakeMove(root, params).gate.name))

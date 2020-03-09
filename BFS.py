import random, os, sys, time
import numpy as np
from operator import attrgetter
from gate import Gate

class Params:
  def __init__(self, weights=[], sp=0.10, lapse_rate=0.05, pruning_threshold=0.0, mu=0.0, sigma=1.0):
    self.weights = weights
    self.stopping_probability = sp
    self.lapse_rate = lapse_rate
    self.pruning_threshold = pruning_threshold
    self.mu = mu
    self.sigma = sigma

class Gate:
  def __init__(self, name = '', begin_time = 0, 
            neighbors = [], edge_dist_tt = [], 
            empty = False, v=0, t=False):
    # self attributes
    self.name = name;
    self.begin_time = begin_time
    self.neighbors = neighbors
    self.edge_dist_tt = edge_dist_tt
    self.empty = empty
    self.value = v
    self.terminate = t

class Node(Gate):
  def __init__(self, gate):
    self.gate = gate
    self.parent = None
    self.children = []
    self.value = self.gate.value
    self.terminate = self.gate.terminate
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

  gate1 = Gate('gate1', 1, [], [])

  gate2 = Gate('empty2', 2, [], [], True)
  gate3 = Gate('gate3', 2, [], [])

  gate4 = Gate('empty4', 3, [], [], True)
  gate5 = Gate('gate5', 3, [], [])
  gate6 = Gate('gate6', 3, [], [])

  gate7 = Gate('empty7', 4, [], [], True)
  gate8 = Gate('gate8', 4, [], [])

  gate9 = Gate('empty9', 5, [], [], True, t=True)
  gate10 = Gate('gate10', 5, [], [], t=True)

  gate1.value = 1
  gate2.value = 2
  gate3.value = 3
  gate4.value = 4
  gate5.value = 5
  gate6.value = 6
  gate7.value = 7
  gate8.value = 8
  gate9.value = 9
  gate10.value = 10

  gate1.neighbors = [gate2,gate3]
  gate2.neighbors = [gate4,gate5,gate6]
  gate3.neighbors = [gate4,gate5,gate6]
  gate4.neighbors = [gate7,gate8]
  gate5.neighbors = [gate7,gate8]
  gate6.neighbors = [gate7,gate8]
  gate7.neighbors = [gate9,gate10]
  gate8.neighbors = [gate9,gate10]

  gate1.edge_dist_tt = [0,.084]
  gate2.edge_dist_tt = [0,0,0]
  gate3.edge_dist_tt = [0,.084,.084]
  gate4.edge_dist_tt = [0,0]
  gate5.edge_dist_tt = [0,.084]
  gate6.edge_dist_tt = [0,.084]
  gate7.edge_dist_tt = [0,0]
  gate8.edge_dist_tt = [0,.084]

  node1 = Node(gate1)
  node2 = Node(gate2)
  node3 = Node(gate3)
  node4 = Node(gate4)
  node5 = Node(gate5)
  node6 = Node(gate6)
  node7 = Node(gate7)
  node8 = Node(gate8)
  node9 = Node(gate9)
  node10 = Node(gate10)


  print("decision: "+str(MakeMove(node1, params).gate.name))














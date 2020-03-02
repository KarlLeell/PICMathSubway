import random, os, sys, time
import numpy as np
from operator import attrgetter

class Params:
  def __init__(self, weights=[], sp=0.10, lapse_rate=0.05, pruning_threshold=0.0, mu=0.0, sigma=1.0):
  	self.weights = weights
  	self.stopping_probability = sp
  	self.lapse_rate = lapse_rate
  	self.pruning_threshold = pruning_threshold
  	self.mu = mu
  	self.sigma = sigma

class Node(Gate):
  def __init__(self, params):
  	self.value = heuristic_value_function(params)
  	self.parent = None
    self.children = []
  def heuristic_value_function(self, params):
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
  for i in range(len(node.neighbors)):
    if (node.neighbors[i].begin_time - node.edge_dist_tt[i] > node.end_time):
      child = Node(node.neighbors[i])
      child.parent = node
      node.children.append(child)
  return node.children

def SelectNode(root):
  ''' return the leaf node along the most promising branch '''
  n = root
  while len(n.children) != 0:
  	n = ArgmaxChild(n)
  return n

def ExpandNode(node, params):
  ''' expand the current node with children, prune '''
  InitializeChildren(node, params)
  Vmaxchild = ArgmaxChild(node)
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
  assert len(root.children) == 0
  if Lapse(params.lapse_rate):
  	return RandomMove(root, params)
  else:
  	while not Stop(params.stopping_probability):
  	  leaf = SelectNode(root)
  	  ExpandNode(leaf, params)
  	  Backpropagate(leaf, root)
  	if root.children == []:
  	  ExpandNode(root, params)
  return ArgmaxChild(root)





















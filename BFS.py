import random, os, sys, time
import numpy as np

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
  	self.value = calc_value()
  	self.parent = None
  def calc_value(self):
  	pass
  def remove_neighbor(self, n):
  	pass

def Lapse(probability):
  ''' return true with a certain probability '''
  return random.random() < probability

def Stop(probability):
  ''' return true with a certain probability '''
  return random.random() < probability

def RandomMove(node, params):
  ''' make a random move '''
  InitializeNeighbors(node, params)
  return random.choice(node.neighbors)

def InitializeNeighbors(node, params):
  pass

def SelectNode(root):
  ''' return the leaf node along the most promising branch '''
  n = root
  while len(n.neighbors) != 0:
  	n = ArgmaxNeighbor(n)
  return n

def ExpandNode(node, params):
  ''' expand the current node with neighbors, prune '''
  InitializeNeighbors(node, params)
  Vmaxneighbor = ArgmaxNeighbor(node)
  Vmax = Vmaxneighbor.value
  for n in node.neighbors:
  	  if abs(n.value - Vmax) > params.pruning_threshold:
  	  	n.remove_neighbor(n)

def Backpropagate(node, root):
  ''' update value back until root node '''
  node.alue = ArgmaxNeighbor(node).value
  if node != root:
  	Backpropagate(node.parent, root)

def ArgmaxNeighbor(node):
  ''' return the neighbor with max value '''
  return max(node.neighbors, key=attrgetter('value'))

def MakeMove(root, params):
  ''' make an optimal move according to value function '''
  assert len(root.neighbors) == 0
  if Lapse(params.lapse_rate):
  	return RandomMove(root, params)
  else:
  	while not Stop(params.stopping_probability):
  	  leaf = SelectNode(root)
  	  ExpandNode(leaf, params)
  	  Backpropagate(leaf, root)
  	if root.neighbors == []:
  	  ExpandNode(root, params)
  return ArgmaxNeighbor(root)





















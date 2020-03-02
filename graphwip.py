import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def weighted_adjmatrix(adjlist, nodes):
    '''Returns a (weighted) adjacency matrix as a NumPy array, I don't think we need this but it could be useful.'''
    matrix = []
    for node in nodes:
        weights = {endnode:int(weight)
                   for w in adjlist.get(node, {})
                   for endnode, weight in w.items()}
        matrix.append([weights.get(endnode, 0) for endnode in nodes])
    matrix = np.array(matrix)
    return matrix + matrix.transpose()
    
    
H=nx.Graph(adjmatrix)
plt.title('title')
nx.draw(H, with_labels=True, node_size=100, node_color="skyblue")
plt.show()

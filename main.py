#Python code investigating the global clustering coefficient of Erdos-REnyi random graphs

import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def testGlobalCluster(n, p, repeats=10):
  L = []
  for _ in range(repeats): #generate a bunch of graphs
    G = nx.gnp_random_graph(n, p)
    C = nx.transitivity(G) #global clustering coefficient is called transitivity in networkx
    L.append(C) #collect their global clustering coefficient
  plt.hist(L, bins=100, density=True)
  plt.title(r'Global Clustering Coefficient of $G_{'+str(n)+','+str(p)+'}$')
  plt.xlabel('Clustering Coefficient')
  plt.ylabel('Probability')
  plt.savefig('Gnp_clustering.png')
  plt.clf()

def readEdgeList(filename):
  G = nx.Graph()
  with open(filename, 'r') as f:
    for line in f:
      l = line.strip().split(' ')
      u = int(l[0])
      v = int(l[1])
      G.add_edge(u, v)
  return G

if __name__=='__main__':
  G = nx.gnp_random_graph(1000, 0.1)
  n = G.number_of_nodes()
  p = 0.1 #make sure that p is above the connectivity threshold
  repeats = 1000
  testGlobalCluster(n, p, repeats=repeats)
  asdffd

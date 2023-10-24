'''
Authors:
* Lucas Butler
* Jacob Collins
* Spencer Pollard
* Suneetha Tadi
Description:
Simulate the Prisoner's Dilemma on randomly generated
networks across many time steps.
Sources:
'''

import networkx as nx
from graph import addAgentsToGraph

if __name__=='__main__':
    G1 = nx.complete_graph(5)
    addAgentsToGraph(G1, 0, [1, 0], [0.5, 0.5])
    print("Constant Strategies (Default)")
    for u in G1.nodes():
        print([G1.nodes[u]['agent'].strategy() for _ in range(10)])
    
    print("Probabilistic Strategies")
    G2 = nx.complete_graph(5)
    addAgentsToGraph(G2, 0, [0.8, 0.2], [0.5, 0.5])
    for u in G2.nodes():
        print([G2.nodes[u]['agent'].strategy() for _ in range(10)])
 


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
from graph import configModel

if __name__=='__main__':
    G = configModel(
        [2, 2, 2],
        0,
    )
    print(G.nodes())
    for u in G.nodes():
        print(G.nodes[u]['agent'].test())
    
 

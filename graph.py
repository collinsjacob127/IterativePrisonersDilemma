# Jacob Collins

from node import Node
from networkx import set_node_attributes, neighbors
from numpy.random import choice
#import networkx as nx


# Function for generating a network of agents using config model
# @param deg_seq: 1d list of the degree for node u in range(len(deg_seq))
# @param init_score: the score to set the initial value of prisoners to
# @param coop_vals: list of possible starting coop_probs for prisoners
# @param coop_odds: probability of a node having the coop_prob assosciated with
#                   the corresponding index in coop_vals
def addAgentsToGraph(
    G, 
    init_score=0, 
    coop_vals=[1, 0], 
    coop_odds=[0.5, 0.5]):
    attrs = {
        u: Node(
            score=init_score, 
            coop_prob=choice(
                coop_vals,
                1, 
                p=coop_odds)
            ) 
        for u in G.nodes()
    }
    set_node_attributes(G, attrs, 'agent')
    return G
    
def updateScores(G):
    for u in G.nodes():
        for v in neighbors(G, u):
            G.nodes[u]['agent'].updateScore(G.nodes[v]['agent'])

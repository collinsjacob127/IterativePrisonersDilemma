# Jacob Collins

from node import Node
from networkx import set_node_attributes, neighbors, get_node_attributes
from numpy.random import choice
#import networkx as nx


# Function for generating a network of agents using config model
# @param deg_seq: 1d list of the degree for node u in range(len(deg_seq))
# @param init_score: the score to set the initial value of prisoners to
# @param coop_vals: list of possible starting coop_probs for prisoners
# @param coop_odds: probability of a node having the coop_prob assosciated with
#                   the corresponding index in coop_vals
def add_rand_agents(
    G, 
    init_score=0, 
    coop_vals=[1, 0], 
    coop_odds=[0.5, 0.5],
    tag='agent'):
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
    set_node_attributes(G, attrs, tag)
    return G

def get_agent(G, u, tag='agent'):
    return G.nodes[u][tag]
    
def update_scores(
    G, 
    n_bunch=None, 
    agent_tag='agent', 
    score_tag='score'):
    S = G.subgraph(n_bunch).copy()
    for u in S.nodes():
        for v in neighbors(S, u):
            S.nodes[u]['agent'].update_score(S.nodes[v][agent_tag])
    scores = {u: get_agent(G, u).get_score() for u in S}
    set_node_attributes(G, scores, score_tag)




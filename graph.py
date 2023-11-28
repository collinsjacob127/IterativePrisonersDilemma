# Author: Jacob Collins

from node import Node
from networkx import set_node_attributes, neighbors, get_node_attributes
from numpy.random import choice
from collections.abc import Iterable
#import networkx as nx


'''
Function for generating a network of agents
@param G: A graph to add agents to the nodes of
@param init_score: the score to set the initial value of prisoners to
@param coop_vals: list of possible starting coop_probs for prisoners
@param coop_odds: probability of a node having the coop_prob assosciated with
                  the corresponding index in coop_vals
Agents are initialized with randomized scores and coop probs based on 
  our defined probability distribution and matching coop_prob list
@return G: The input graph, with agents in G.node[u][tag]
'''
def add_rand_agents(
    G, 
    init_score=0, 
    coop_vals=[1, 0], 
    coop_odds=[0.5, 0.5],
    tag='agent'):
    attrs = {
        u: Node(
            id=u,
            score=init_score, 
            coop_prob=float(choice(
                coop_vals,
                1, 
                p=coop_odds)))
        for u in G.nodes()
    }
    set_node_attributes(G, attrs, tag)
    return G

  
# Agents are initialized with individual predefined scores and coop_probs
# @return G: The input graph, with agents in G.node[u][tag]
def add_agents(
    G, 
    score_vals,
    coop_vals, 
    tag='agent'):
    num_nodes = len(G.nodes())
    if not isinstance(score_vals, Iterable):
        score_vals = [score_vals] * num_nodes
    if not isinstance(coop_vals, Iterable):
        coop_vals = [coop_vals] * num_nodes
    attrs = {
        u: Node(
            id=u,
            score=score_vals[i], 
            coop_prob=coop_vals[i]) 
        for i, u in enumerate(G.nodes())}
    set_node_attributes(G, attrs, tag)
    return G


def get_agent(G, u, tag='agent'):
    return G.nodes[u][tag]
    

def update_score_attribute(G, score_tag='score', strategy_tag='strategy'):
    scores = {u: get_agent(G, u).get_score() for u in G}
    strategies = {u: get_agent(G, u).get_coop_prob() for u in G}
    set_node_attributes(G, scores, score_tag)
    set_node_attributes(G, strategies, strategy_tag)
    

def update_scores(
    G, 
    n_bunch=None, 
    kill=False,
    kill_score_cap = 100,
    takeover=True,
    agent_tag='agent', 
    score_tag='score',
    strategy_tag='strategy'):
    S = G.subgraph(n_bunch).copy()
    if kill:
        nodes_to_remove = [[u, G.nodes[u][agent_tag]] for u in G.nodes() if G.nodes[u][score_tag] > kill_score_cap]
        for u in nodes_to_remove:
            G.remove_node(u[0])

    for u, v in G.edges():
        # Get u and v coop prob, have them play, whoever loses adjust their strategy
        G.nodes[u][agent_tag].update_score(G.nodes[v][agent_tag], takeover=takeover)
    
    update_score_attribute(G)
    return []

def verify_agents(G):
    print([c for c in get_node_attributes(G)])
    
    
def run_time_steps(G, n):
    return

def set_node_positions(G, pos):
    cleaned_pos = {u: tuple(pos[u]) for u in list(pos.keys())}
    set_node_attributes(G, cleaned_pos, 'pos')
    return G


def keep_node_positions(G, pos_dict):
    set_node_attributes(G, pos_dict, 'pos')
    return G

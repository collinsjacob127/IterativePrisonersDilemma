# Jacob Collins

from node import Node
from networkx import Graph, configuration_model
from numpy.random import choice


# Class for generating a network of agents using config model
# @param init_score: the score to set the initial value of prisoners to
# @param coop_vals: list of possible starting coop_probs for prisoners
# @param coop_odds: probability of a node having the coop_prob assosciated with
#                   the corresponding index in coop_vals
def configModel(deg_seq, init_score=0, coop_vals=[1, 0], coop_odds=[0.5, 0.5]):
    network = configuration_model(deg_seq)
    # Initialize Nodes into Network
    for i in range(len(deg_seq)):
        u = Node(score=init_score, coop_prob=choice(coop_vals, 1, p=coop_odds))
        network.add_node(i,data=u)
    print(f'Nodes: {network.nodes}')
    # Generate List from Degree Distribution
    config_list = []
    for i, u in enumerate(network.nodes()):
        config_list += list([u] * deg_seq[i])
    print(config_list)
    # Add random edges (no loops)
    while len(config_list) > 0:
        print(f'Config list: {config_list}')
        pair = choice(config_list, 2, replace=False)
        if pair[0] == pair[1]:
            continue
        network.add_edge(pair[0], pair[1])
        config_list.remove(pair[0])
        config_list.remove(pair[1])
        
    
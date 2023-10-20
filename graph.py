# Jacob Collins

from node import Node
from networkx import Graph
from numpy.random import choice


# Class for generating a network of agents using config model
# @param init_score: the score to set the initial value of prisoners to
# @param coop_vals: list of possible starting coop_probs for prisoners
# @param coop_odds: probability of a node having the coop_prob assosciated with
#                   the corresponding index in coop_vals
class configModel():

    network = Graph()

    def __init__(self, deg_seq, init_score=0, coop_vals=[1, 0], coop_odds=[0.5, 0.5]):
        # Initialize Nodes into Network
        for _ in range(len(deg_seq)):
            self.network.add_node(Node(score=init_score, coop_prob=choice(coop_vals, 1, p=coop_odds)))
        print(self.network.nodes())
        # Generate List from Degree Distribution
        config_list = [[u] * deg_seq[i] for i, u in enumerate(self.network.nodes())]
        print(config_list)
        # Add random edges (no self-loops)
        while len(config_list) > 0:
            pair = choice(config_list, 2, replace=False)
            if pair[0] == pair[1]:
                continue
            self.network.add_edge(pair[0], pair[1])
        
    def __repr__(self):
        print(f'Nodes:\n{self.network.nodes()}\nEdges:\n{self.network.edges()}')
    
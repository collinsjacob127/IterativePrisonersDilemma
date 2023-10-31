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
from graph import *
from save import *

def example():
    G1 = nx.complete_graph(6)
    add_agents(G1, 0, [1,1,1,0,0,0])
    print("Constant Strategies (Default)")
    for u in G1.nodes():
        print(f'{u}: {get_agent(G1, u)}')
    print("")
    # update_scores(G1, [1, 2]) # Updates the scores of nodes 1 and 2
    update_scores(G1) # Updates the scores
    for u in G1.nodes():
        print(f'Data of Agent {u}: {get_agent(G1, u)}') # Agent class is returned (Shows __repr__)
    print(f'Scores (nx dict): {nx.get_node_attributes(G1, "score")}') # Showing that score is also saved in the node itself
    print(f'Strategies (nx dict): {nx.get_node_attributes(G1, "strategy")}') # Showing that score is also saved in the node itself
    print("")
    
    print("Probabilistic Strategies")
    G2 = nx.complete_graph(5)
    add_rand_agents(G2, 0, [0.8, 0.2], [0.5, 0.5])
    for u in G2.nodes():
        print(f'{u}: {get_agent(G2, u)}')
    print("")
    update_scores(G2)
    for u in G2.nodes():
        print(f'Data of Agent {u}: {get_agent(G2, u)}') # Agent class is returned (Shows __repr__)
    print(f'Scores (nx dict): {nx.get_node_attributes(G2, "score")}') # Showing that score is also saved in the node itself
    print(f'Strategies (nx dict): {nx.get_node_attributes(G2, "strategy")}') # Showing that score is also saved in the node itself
    print("")

# Generates a GIF of the simulation's time steps
# 90% of prisoners have an 80% chance to cooperate
# 10% of prisoners have a 20% chance to cooperate
def generate_gif():
    G = nx.gnp_random_graph(100, 0.05, seed=1)
    add_rand_agents(G, 0.0, [0.8, 0.2], [0.9, 0.1])
    # pos = nx.spectral_layout(G)
    pos = nx.shell_layout(G)
    G = set_node_positions(G, pos)
    pos_dict = get_node_attributes(G, 'pos')
    for i in range(40):
        G = update_scores(G, kill=True, kill_score_cap=150)
        G = keep_node_positions(G, pos_dict)
        draw_graph(G, f'{i}_varying_prisoner_strat', 'complete/test1', "Test Plot")
    nx.set_node_attributes(G, None, 'agent')
    for u in G.nodes():
        del G.nodes[u]['agent']
    save_gif('varying_prisoner_strat', 'complete/test1')
    

if __name__=='__main__':
    n = 10

    generate_gif()

    # G1 = nx.path_graph(n)
    # add_agents(G1, 0.0, [1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0])
    # # update_scores(G1, [1, 2]) # Updates the scores of nodes 1 and 2
    # for _ in range(5):
    #     update_scores(G1, score_tag='years_assigned')
    # nx.set_node_attributes(G1, None, 'agent')
    # for u in G1.nodes():
    #     del G1.nodes[u]['agent']
    # nx.write_gexf(G1, "graphs/path_constant_strat.gexf")

    # print("Probabilistic Strategies")
    # G2 = nx.complete_graph(100)
    # add_rand_agents(G2, 0.0, [1.0, 0.0], [0.5, 0.5])
    # for _ in range(5):
    #     update_scores(G2)
    # nx.set_node_attributes(G2, None, 'agent')
    # for u in G2.nodes():
    #     del G2.nodes[u]['agent']
    # nx.write_gexf(G2, "graphs/varying_prisoner_strat.gexf")
    # save_gexf(G2, 'varying_prisoner_strat.gexf', 'complete')
    # draw_graph(G2, 'varying_prisoner_strat.gexf', 'complete')


    # G1 = nx.path_graph(n)
    # add_agents(G1, 0.0, [1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0])
    # # update_scores(G1, [1, 2]) # Updates the scores of nodes 1 and 2
    # for _ in range(5):
    #     update_scores(G1, score_tag='years_assigned')
    # nx.set_node_attributes(G1, None, 'agent')
    # for u in G1.nodes():
    #     del G1.nodes[u]['agent']
    # nx.write_gexf(G1, "graphs/path_constant_strat.gexf")
    

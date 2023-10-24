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
from graph import add_rand_agents, add_agents, update_scores, get_agent

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


if __name__=='__main__':
    n = 10
    G1 = nx.complete_graph(n)
    add_agents(G1, 0, [1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0])
    # update_scores(G1, [1, 2]) # Updates the scores of nodes 1 and 2
    for _ in range(5):
        update_scores(G1, score_tag='years_assigned')
    nx.set_node_attributes(G1, None, 'agent')
    for u in G1.nodes():
        del G1.nodes[u]['agent']
    nx.write_gexf(G1, "path_constant_strat.gexf")
    
    print("Probabilistic Strategies")
    G2 = nx.path_graph(10)
    add_rand_agents(G2, 0, [0.8, 0.2], [0.5, 0.5])
    for _ in range(5):
        update_scores(G2, score_tag='years_assigned')
    nx.set_node_attributes(G2, None, 'agent')
    for u in G2.nodes():
        del G2.nodes[u]['agent']
    nx.write_gexf(G2, "varying_prisoner_strat.gexf")

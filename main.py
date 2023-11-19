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
from numpy import floor, mean
from graph import *
from save import *

def example():
    n = 6
    G1 = nx.complete_graph(n)
    coop_prop = 0.9
    n_coop = int(floor(n*coop_prop))
    add_agents(G1, 0, [0.8]*n_coop + [0.2]*(n-n_coop))
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
    G2 = nx.complete_graph(n)
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
    n = 20
    # G = nx.complete_graph(n)
    G = nx.gnp_random_graph(n, 5/(n+5), seed=1)
    add_rand_agents(G, 0.0, [0.8, 0.2], [0.9, 0.1])
    coop_prop = 0.5
    n_coop = int(floor(n*coop_prop))
    # add_agents(G, 0, [0.8]*n_coop + [0.2]*(n-n_coop))
    add_agents(G, 0, [1.0]*n_coop + [0.0]*(n-n_coop))

    # pos = nx.spectral_layout(G)
    pos = nx.shell_layout(G)
    G = set_node_positions(G, pos)
    pos_dict = get_node_attributes(G, 'pos')
    update_score_attribute(G)
    removed_nodes = []
    for i in range(40):
        removed_nodes += update_scores(G, kill=True, kill_score_cap=700)
        G = keep_node_positions(G, pos_dict)
        draw_graph(G, f'{i}_varying_prisoner_strat', 'complete/test1', "Simulating the Prisoner's Dilemma")
    print("Dead:")
    for u in removed_nodes:
        print(u)
    print("Alive:")
    for u in G.nodes():
        print(G.nodes[u]['agent'])
    save_gif('varying_prisoner_strat', dirname='gnp', filename='test1')
    
def test_proportions():
    n = 100
    # G = nx.gnp_random_graph(n, 0.05)
    max_degree = 10
    for k in range(2, 6):
        # G = nx.configuration_model([np.random.choice(list(range(1,max_degree))) for _ in range(n)])
        # deg_seq = np.random.poisson(k, size=n).tolist()
        deg_seq = [k]*n
        if sum(deg_seq) % 2 != 0:
            deg_seq[0] += 1
        G = nx.configuration_model(deg_seq)
        y_lists = [[], [], []]
        x_list = [0.05 * i for i in range(21)]
        for coop_prop in x_list:
            n_coop = int(floor(n*coop_prop))
            add_agents(G, 0, [1.0]*n_coop + [0.0]*(n-n_coop))

            for _ in range(40):
                update_scores(G, takeover=False)

            coop_years = []
            defect_years = []
            for u in G.nodes():
                node = G.nodes[u]['agent']
                if node.get_coop_prob() >= 0.5:
                    coop_years.append(node.get_score())
                else:
                    defect_years.append(node.get_score())

            print(f'coop_prob: {mean(coop_prop)}')
            print(f'    defect_years: {mean(defect_years)}')
            if len(defect_years) > 0:
                y_lists[0].append(mean(defect_years))
            else:
                y_lists[0].append(0)
            print(f'    coop_years: {mean(coop_years)}')
            if len(coop_years) > 0:
                y_lists[1].append(mean(coop_years))
            else:
                y_lists[1].append(0)
            y_lists[2].append((y_lists[0][len(y_lists[0])-1]+y_lists[1][len(y_lists[0])-1])/2)
        compareLines(
            x_list=x_list,
            y_lists=y_lists,
            y_labels=[
                "Defectors",
                "Cooperators",
                "All Agents"
            ],
            xlabel="Proportion of Cooperators",
            ylabel="Years Assigned",
            name=f'poisson_config_{k}',
            dirname=f'new_compare',
            title=f"Years Assigned - Config Model, Uniform k={k}",
            subtitle="Average Years Assigned in Each Group"
        )
    
def test_takeover():
    n = 100
    G = nx.gnp_random_graph(n, 0.05)
    max_degree = 10
    for k in range(2, 6):
        # G = nx.configuration_model([np.random.choice(list(range(1,max_degree))) for _ in range(n)])
        # deg_seq = np.random.poisson(k, size=n).tolist()
        # if sum(deg_seq) % 2 != 0:
        #     deg_seq[0] += 1
        # G = nx.configuration_model(deg_seq)
        prop_list = [0.05 * i for i in range(21)]
        for coop_prop in prop_list:
            n_coop = int(floor(n*coop_prop))
            add_agents(G, 0, [1.0]*n_coop + [0.0]*(n-n_coop))

            n_iter=40
            x_list = range(n_iter)
            y_lists = []
            for _ in range(n):
                y_lists.append([])
            for _ in range(n_iter):
                update_scores(G)

                for u in G.nodes():
                    node = G.nodes[u]['agent']
                    y_lists[u].append(node.get_coop_prob())
            manyLines(
                x_list=x_list,
                y_lists=y_lists,
                yrange=(-0.02, 1.02),
                xlabel="Time Step",
                ylabel="Cooperation Probability",
                name=f'gnp_takeover_{coop_prop}',
                title=f"Development of Takeover",
                subtitle=r"$G_{" + f"{n},{np.round(coop_prop,1)}" + r"}$",
            )

if __name__=='__main__':
    n = 10

    # test_proportions()
    test_takeover()
    # generate_gif()

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

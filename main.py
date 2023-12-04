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
from helpers import *

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
    n = 100
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
        removed_nodes += update_scores(G, kill=True, kill_score_cap=500)
        G = keep_node_positions(G, pos_dict)
        draw_graph(G, f'{i}_varying_prisoner_strat', 'gnp/test1', "Simulating the Prisoner's Dilemma")
    print("Dead:")
    for u in removed_nodes:
        print(u)
    print("Alive:")
    for u in G.nodes():
        print(G.nodes[u]['agent'])
    save_gif('varying_prisoner_strat', dirname='gnp/test1')
    
def test_proportions(G, n, dir_graph_name, graph_type):
    # G = nx.gnp_random_graph(n, 0.05)
    n_iter = 10
    y_lists = [[], [], []]
    x_list = [0.005 * i for i in range(4)] + [0.02 * i for i in range(1, 51)]
    print(f"Testing Proportions on {graph_type}")
    for coop_prop in x_list:
        coop_full_years = []
        defect_full_years = []
        printProgressBar(
            iteration=0, 
            total=n_iter, 
            suffix=f"Starting Coop: {round(coop_prop*100,1)}%",
            length=25)
        for i in range(n_iter):
            coop_full_years.append([])
            defect_full_years.append([])
            n_coop = int(floor(n*coop_prop))
            add_agents(G, 0, [1.0]*n_coop + [0.0]*(n-n_coop))
            for _ in range(20):
                update_scores(G, takeover=False)
            for u in G.nodes():
                node = G.nodes[u]['agent']
                if node.get_coop_prob() >= 0.5:
                    coop_full_years[i].append(node.get_score())
                else:
                    defect_full_years[i].append(node.get_score())
            coop_years = mean_across_lists(coop_full_years)
            defect_years = mean_across_lists(defect_full_years)
            printProgressBar(
                iteration=i, 
                total=n_iter, 
                suffix=f"Starting Coop: {round(coop_prop*100,1)}%",
                length=25)
        # print(f'coop_prob: {mean(coop_prop)}')
        # print(f'    defect_years: {mean(defect_years)}')
        if len(defect_years) > 0:
            y_lists[0].append(mean(defect_years))
        else:
            y_lists[0].append(0)
        # print(f'    coop_years: {mean(coop_years)}')
        if len(coop_years) > 0:
            y_lists[1].append(mean(coop_years))
        else:
            y_lists[1].append(0)
        y_lists[2].append((y_lists[0][len(y_lists[0])-1]+y_lists[1][len(y_lists[0])-1])/2)
    printProgressBar(
        iteration=n_iter, 
        total=n_iter, 
        suffix=f"Starting Coop: {round(coop_prop*100,1)}%",
        length=25)
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
        name=f'proportions',
        dirname=f'figs/test_proportions/{dir_graph_name}',
        darktheme=False,
        title=f"Years Assigned - {graph_type}",
        subtitle="Average Years Assigned in Each Group"
    )
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
        name=f'dark_proportions',
        darktheme=True,
        dirname=f'figs/test_proportions/{dir_graph_name}',
        title=f"Years Assigned - {graph_type}",
        subtitle="Average Years Assigned in Each Group"
    )

def test_takeover(G, n, dir_graph_name, graph_type):
    prop_list = [(1/25) * i for i in range(26)] # 0.2, 0.4, ..., 1.0
    n_iter=40
    x_list = range(n_iter)
    y_lists = []
    print(f"Testing Takeover on {graph_type}")
    for i, coop_prop in enumerate(prop_list):
        y_lists.append([])
        n_coop = int(floor(n*coop_prop))
        add_agents(G, 0, [1.0]*n_coop + [0.0]*(n-n_coop))
        printProgressBar(
            iteration=0, 
            total=n_iter, 
            suffix=f"Starting Coop: {round(coop_prop*100,1)}%",
            length=25)
        for j in range(n_iter):
            y_lists[i].append(np.mean([node.get_coop_prob() for node in [G.nodes[u]['agent'] for u in G.nodes()]]))
            update_scores(G)
            printProgressBar(
                iteration=j, 
                total=n_iter, 
                suffix=f"Starting Coop: {round(coop_prop*100,1)}%",
                length=25)
    printProgressBar(
        iteration=n_iter, 
        total=n_iter, 
        suffix=f"Starting Coop: {round(coop_prop*100,1)}%",
        length=25)
    compareLines(
        x_list=x_list,
        y_lists=y_lists,
        yrange=(-0.02, 1.02),
        xlabel="Time Step",
        ylabel="Mean Cooperation Probability",
        # y_labels=[f"{np.round(prop*100, 2)}% Cooperators" for prop in prop_list],
        dirname=f"figs/takeover/{dir_graph_name}",
        name=f'takeover',
        size=3,
        darktheme=False,
        title=f"Development of Takeover",
        subtitle=f"100 Nodes on {graph_type}"
    )
    compareLines(
        x_list=x_list,
        y_lists=y_lists,
        yrange=(-0.02, 1.02),
        xlabel="Time Step",
        ylabel="Mean Cooperation Probability",
        # y_labels=[f"{np.round(prop*100, 2)}% Cooperators" for prop in prop_list],
        dirname=f"figs/takeover/{dir_graph_name}",
        name=f'dark_takeover',
        size=3,
        darktheme=True,
        title=f"Development of Takeover",
        subtitle=f"100 Nodes on {graph_type}"
    )

if __name__=='__main__':
    n = 100
    for k in [2,3,4,5]:
        deg_seq = [k] * n
        if sum(deg_seq) % 2 != 0:
            deg_seq[0] += 1
        G = nx.configuration_model(deg_seq)
        dirname = f"config_{n}_{k}"
        graph_type = f"Config Model, k={k}, n={n}"
        test_proportions(G, n, dirname, graph_type)
        test_takeover(G, n, dirname, graph_type)
    n = 1000
    for k in [2,3,4,5]:
        deg_seq = [k] * n
        if sum(deg_seq) % 2 != 0:
            deg_seq[0] += 1
        G = nx.configuration_model(deg_seq)
        dirname = f"config_{n}_{k}"
        graph_type = f"Config Model, k={k}, n={n}"
        test_proportions(G, n, dirname, graph_type)
        test_takeover(G, n, dirname, graph_type)

    n = 100
    G = nx.gnp_random_graph(n, 0.05)
    dirname = "gnp_100_05"
    graph_type = r"Erdős–Rényi Random Graph, $G_{100,0.05}$"
    test_proportions(G, n, dirname, graph_type)
    test_takeover(G, n, dirname, graph_type)

    n = 1000
    G = nx.gnp_random_graph(n, 0.05)
    dirname = f"gnp_1000_05"
    graph_type = r"Erdős–Rényi Random Graph, $G_{1000,0.05}$"
    test_proportions(G, n, dirname, graph_type)
    test_takeover(G, n, dirname, graph_type)

    n = 100
    for m in [2,3,4]:
        dirname = f"barabasi_albert_{n}_{m}"
        graph_type = r"Barabasi-Albert Random Graph, $G_{" + f'{n}, {m}' + r"}$"
        G = nx.barabasi_albert_graph(n, m)
        test_proportions(G, n, dirname, graph_type)
        test_takeover(G, n, dirname, graph_type)

    n = 500
    for m in [2,3,4]:
        dirname = f"barabasi_albert_{n}_{m}"
        graph_type = r"Barabasi-Albert Random Graph, $G_{" + f'{n}, {m}' + r"}$"
        G = nx.barabasi_albert_graph(n, m)
        test_proportions(G, n, dirname, graph_type)
        test_takeover(G, n, dirname, graph_type)
    
    n = 100
    G = nx.complete_graph(n)
    dirname = f"complete_{n}"
    graph_type = r"Complete Graph, $K_{" + f'{n}' + r"}$"
    test_proportions(G, n, dirname, graph_type)
    test_takeover(G, n, dirname, graph_type)

    n = 1000
    G = nx.complete_graph(n)
    dirname = f"complete_{n}"
    graph_type = r"Complete Graph, $K_{" + f'{n}' + r"}$"
    test_proportions(G, n, dirname, graph_type)
    test_takeover(G, n, dirname, graph_type)
    
    

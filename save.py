# Author: Jacob Collins
# Sources: 
# * [Plotly Tutorial](https://plotly.com/python/network-graphs/)

from os import makedirs, listdir, getcwd
from networkx import write_gexf, set_node_attributes, shell_layout
from graph import set_node_positions
import plotly.graph_objects as go
import imageio
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import os


# Save the graph in gexf format
def save_gexf(G, filename, dirname):
    makedirs(f'graphs/{dirname}', exist_ok=True)
    write_gexf(G, f"graphs/{dirname}/{filename}.gexf")

# Save figures of the graph using plotly
# @param G: The graph to plot 
# @param filename: The name of the png, don't give the extension.
# @param dirname: Subdirectories in which 
#                 to save the graph images. 
#                 Given in the form 'dir1/dir2' or 'dirname'
#                 (No trailing forward-slash) (Optional)
# @param pos: The networkx positional layout for the graph (Optional)
def draw_graph(G, filename, dirname=None, title=None):
    kill_score_cap=200
    # Add edges to plot
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='White'),
        # line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    # Add nodes to plot
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='Portland',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                tick0=0,
                dtick=20,
                thickness=15,
                tickfont=dict(
                        family="Courier New, monospace",
                        size=14,
                        color="LightGray"
                        ),
                title={
                    'text': 'Years Imprisoned',
                    'font': dict(
                        family="Courier New, monospace",
                        size=20,
                        color="LightGray"
                    )},
                xanchor='left',
                titleside='right',
                x=1
            ),
            line_width=2))
    # Color Node Points
    node_scores = []
    node_text = []
    for node in G.nodes():
        node_scores.append(G.nodes[node]['score'])
        node_text.append(f'Score: {G.nodes[node]["score"]}')

    node_trace.marker.color = node_scores
    node_trace.text = node_text
    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                # annotations=[ dict(
                #     text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                #     showarrow=False,
                #     xref="paper", yref="paper",
                #     x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    # Title format and positioning
    fig.update_layout(
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        title={
            'text': "Simulating the Prisoner's Dilemma",
            'font': dict(
                family="Courier New, monospace",
                size=30,
                color="White"
            ),
            'y': 0.97,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top' })
    dir_path = f'graphs/{dirname}/'
    makedirs(dir_path, exist_ok=True)
    fig.write_image(f'{dir_path}{filename}.png', format='png', width=1024, height=768)


def sort_by_prefix(filenames, prefix_list):
    filenames_out = []
    for prefix in prefix_list:
        for file in filenames:
            if file.startswith(prefix):
                filenames_out.append(file)
    return filenames_out
    
def save_gif(filename_skeleton, dirname='test1', filename='test'):
    makedirs(f'graphs/{dirname}', exist_ok=True)
    pathname = f'{getcwd()}/graphs/{dirname}'
    filenames = [file for file in listdir(pathname) if file.endswith('.png')]
    filtered_files = [
        f'{pathname}/{file}' 
        for file in sort_by_prefix(filenames, [f'{i}_' for i in range(len(filenames))])]
    images = [imageio.imread(filename) for filename in filtered_files]
    imageio.mimsave(f'{pathname}/{filename_skeleton}.gif', images)

def compareScatter(
    x_list,
    y_lists,
    titles=None,
    xlabel=None,
    ylabel=None,
    name="temp_filename",
    main_title=None,
):
    x_len = len(x_list)
    for y_list in y_lists:
        if len(y_list) != x_len:
            print(
                f"Array size mismatch in {main_title}"
                + f"\ny len {len(y_list)} != {x_len}"
            )

    color_options = [
        "orangered",
        "mediumturquoise",
        "darkviolet",
        "darkgreen",
        "lime",
        "gold",
        "ivory",
        "black",
        "slateblue",
    ]
    fig, ax = plt.subplots(1, 1, figsize=(10, 5), dpi=300)
    if titles == None:
        for i, y_list in enumerate(y_lists):
            # ax.scatter(
            #     x_list, y_list,
            #     color=color_options[i],
            #     alpha=0.5,
            # )
            ax.fill_between(
                x_list,
                y_list,
                color=color_options[i],
                alpha=0.3,
                edgecolor="black",
                linewidth=0.5,
            )
    else:
        for i, title in enumerate(titles):
            # ax.scatter(
            #     x_list, y_lists[i],
            #     color=color_options[i],
            #     alpha=0.5,
            #     label=title,
            # )
            ax.fill_between(
                x_list,
                y_lists[i],
                color=color_options[i],
                alpha=0.3,
                edgecolor="black",
                linewidth=0.5,
                label=title,
            )
        ax.legend()
    ax.grid(
        visible=True,
    )
    if main_title != None:
        plt.title(f"{main_title}")
    if xlabel != None:
        plt.xlabel(xlabel)
    if ylabel != None:
        plt.ylabel(ylabel)
    try:
        os.mkdir("figs")
    except FileExistsError:
        pass
    plt.savefig(f"figs/{name}.png")
    plt.clf()
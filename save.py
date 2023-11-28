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
    
def save_gif(filename_skeleton, dirname='test1'):
    print(f'Save Gif')
    makedirs(f'graphs/{dirname}', exist_ok=True)
    # pathname = f'{getcwd()}/graphs/{dirname}/'
    pathname = f'graphs/{dirname}/'
    print(f'Dir contents:\n{listdir(pathname)}')
    filenames = [file for file in listdir(pathname) if file.endswith('.png')]
    print(f"Found filenames:\n{filenames}")
    filtered_files = [
        f'{pathname}/{file}' 
        for file in sort_by_prefix(filenames, [f'{i}_' for i in range(len(filenames))])]
    print(f"Filtered files:\n{filtered_files}")
    images = [imageio.imread(filename) for filename in filtered_files]
    imageio.mimsave(f'{pathname}/{filename_skeleton}.gif', images)

def get_color(i, darktheme=False):
    color_options = [
        "#000000", # Black
        "#92140C", # Red
        "#390099", # Purple
        "#F5853F", # Orange
        "#2E86AB", # Blue
    ]
    if darktheme:
        color_options = [
            "#FFFFFF", # White
            "#A4243B", # Red
            "#2B9720", # Green
            "#D8973C", # Orange
            "#45A3D9", # Blue
        ]
    return color_options[i % len(color_options)]
    
    
def compareScatter(
    x_list,
    y_lists,
    y_labels=None,
    title=None,
    subtitle=None,
    xlabel=None,
    ylabel=None,
    logx=False,
    logy=False,
    xrange=None, #Tuple
    yrange=None, #Tuple
    legend_pos=0,
    size=10,
    darktheme=False,
    name="temp_filename",
    dirname="figs",
):
    x_len = len(x_list)
    for y_list in y_lists:
        if len(y_list) != x_len:
            print(
                f"Array size mismatch in {title}"
                + f"\ny len {len(y_list)} != {x_len}"
            )

    alpha = 0.8
    if len(y_lists) > 1:
        alpha = 0.3
    fig, ax = plt.subplots(1, 1, figsize=(10, 5), dpi=300)
    # Set up Axis Definition
    min_x = min(x_list)
    max_x = max(x_list)
    min_y = min([min(y_list) for y_list in y_lists])
    max_y = max([max(y_list) for y_list in y_lists]) 
    max_y = max_y + (max_y - min_y)*0.05 # 5% vertical buffer
    if (xrange):
        min_x = xrange[0]
        max_x = xrange[1]
    if (yrange):
        min_y = yrange[0]
        max_y = yrange[1]
    ax.axis([
        min_x,
        max_x,
        min_y,
        max_y])
    fg_color = 'white'
    fg_color2 = 'grey'
    bg_color='black'
    if darktheme:
        fg_color = 'black'
        fg_color2 = 'grey'
        bg_color='white'
    ax.patch.set_facecolor(bg_color)
    ax.tick_params(color=fg_color, labelcolor=fg_color)
    for spine in ax.spines.values():
        spine.set_edgecolor(fg_color)
    fig.patch.set_facecolor(bg_color)
    ax.grid(
        visible=True,
        alpha=0.7,
        color=fg_color,
        linewidth=0.5,
    )
    
    if y_labels == None:
        for i, y_list in enumerate(y_lists):
            ax.fill_between(
                x_list,
                y_list,
                color=get_color(i, darktheme),
                alpha=alpha,
                edgecolor=get_color(i, darktheme),
                linewidth=0.5,
            )
            ax.scatter(
                x_list, y_list,
                color=get_color(i, darktheme),
                s=size,
                alpha=alpha + ((1-alpha)/2),
            )
    else:
        for i, label in enumerate(y_labels):
            ax.fill_between(
                x_list,
                y_lists[i],
                color=get_color(i, darktheme),
                alpha=alpha,
                edgecolor=get_color(i, darktheme),
                linewidth=0.5,
                label=label,
            )
            ax.scatter(
                x_list, y_lists[i],
                color=get_color(i, darktheme),
                alpha=alpha + ((1-alpha)/2),
                s=size,
            )
        ax.legend(loc=legend_pos)
    # if len(y_lists) == 1 and label_vals:
    #     for i, x in enumerate(x_list):
    #         text_str = f'{np.round(y_lists[0][i], 2).__float__()}'
    #         flip = 1 # 1 => left side, 0 => right side
    #         if i == 0:
    #             flip = 0 # First label should be right of point
    #         elif i < len(x_list)-1 and i > 0:
    #             if y_list[i] < y_list[i-1]: # Was decreasing, don't put left
    #                 flip = 0
    #         if flip:
    #             x_offset = -1*(len(text_str)+0.5)*size*2
    #         ax.annotate(
    #             text_str,
    #             (x, y_lists[0][i]),
    #             # xytext=(-len(text_str)*size,-0.5*size),
    #             xytext=(x_offset,0),
    #             textcoords="offset pixels",
    #             color=fg_color,
    #             fontsize=8)
    if title:
        if subtitle:
            mid = (fig.subplotpars.right + fig.subplotpars.left)/2
            plt.title(f"{subtitle}", color=fg_color2, size=12)
            plt.suptitle(f"{title}", color=fg_color, size=18, x=mid)
        else:
            plt.title(f"{title}", color=fg_color, size=18)
    if xlabel:
        if logx:
            plt.xscale('log')
            plt.xlabel(f'Log {xlabel}', color=fg_color)
        else:
            plt.xlabel(xlabel, color=fg_color)
    if ylabel:
        if logy:
            plt.yscale('log')
            plt.ylabel(f'Log {ylabel}', color=fg_color)
        else:
            plt.ylabel(ylabel, color=fg_color)
    svgdirname = dirname + "-svg" 
    try:
        os.mkdir(dirname)
        os.mkdir(svgdirname)
    except FileExistsError:
        pass
    plt.savefig(f"{dirname}/{name}.png")
    plt.savefig(f"{svgdirname}/{name}.svg", format='svg')
    plt.clf()
    plt.close()

def compareLines(
    x_list,
    y_lists,
    y_labels=None,
    title=None,
    subtitle=None,
    xlabel=None,
    ylabel=None,
    logx=False,
    logy=False,
    xrange=None, #Tuple
    yrange=None, #Tuple
    legend_pos=0,
    size=10,
    darktheme=False,
    name="temp_filename",
    dirname="figs",
):
    x_len = len(x_list)
    for y_list in y_lists:
        if len(y_list) != x_len:
            print(
                f"Array size mismatch in {title}"
                + f"\ny len {len(y_list)} != {x_len}"
            )

    alpha = 0.8
    if len(y_lists) > 1:
        alpha = 0.3
    fig, ax = plt.subplots(1, 1, figsize=(10, 5), dpi=300)
    # Set up Axis Definition
    min_x = min(x_list)
    max_x = max(x_list)
    min_y = min([min(y_list) for y_list in y_lists])
    max_y = max([max(y_list) for y_list in y_lists]) 
    max_y = max_y + (max_y - min_y)*0.05 # 5% vertical buffer
    if (xrange):
        min_x = xrange[0]
        max_x = xrange[1]
    if (yrange):
        min_y = yrange[0]
        max_y = yrange[1]
    ax.axis([
        min_x,
        max_x,
        min_y,
        max_y])
    fg_color = 'black'
    fg_color2 = '#1a1a1a'
    bg_color='white'
    if darktheme:
        fg_color = 'white'
        fg_color2 = '#D9D9D9'
        bg_color='black'
    ax.patch.set_facecolor(bg_color)
    ax.tick_params(color=fg_color, labelcolor=fg_color)
    for spine in ax.spines.values():
        spine.set_edgecolor(fg_color)
    fig.patch.set_facecolor(bg_color)
    ax.grid(
        visible=True,
        alpha=0.7,
        color=fg_color,
        linewidth=0.5,
    )
    
    if y_labels == None:
        for i, y_list in enumerate(y_lists):
            ax.plot(
                x_list,
                y_list,
                color=get_color(i, darktheme),
                alpha=alpha,
                # edgecolor="black",
                linewidth=2,
            )
            ax.scatter(
                x_list, y_list,
                color=get_color(i, darktheme),
                s=size,
                alpha=alpha + ((1-alpha)/2),
            )
    else:
        for i, label in enumerate(y_labels):
            ax.plot(
                x_list,
                y_lists[i],
                color=get_color(i, darktheme),
                alpha=alpha,
                # edgecolor="black",
                linewidth=2,
                label=label,
            )
            ax.scatter(
                x_list, y_lists[i],
                color=get_color(i, darktheme),
                alpha=alpha + ((1-alpha)/2),
                s=size,
            )
        ax.legend(loc=legend_pos)
    # if len(y_lists) == 1 and label_vals:
    #     for i, x in enumerate(x_list):
    #         text_str = f'{np.round(y_lists[0][i], 2).__float__()}'
    #         flip = 1 # 1 => left side, 0 => right side
    #         if i == 0:
    #             flip = 0 # First label should be right of point
    #         elif i < len(x_list)-1 and i > 0:
    #             if y_list[i] < y_list[i-1]: # Was decreasing, don't put left
    #                 flip = 0
    #         if flip:
    #             x_offset = -1*(len(text_str)+0.5)*size*2
    #         ax.annotate(
    #             text_str,
    #             (x, y_lists[0][i]),
    #             # xytext=(-len(text_str)*size,-0.5*size),
    #             xytext=(x_offset,0),
    #             textcoords="offset pixels",
    #             color=fg_color,
    #             fontsize=8)
    if title:
        if subtitle:
            mid = (fig.subplotpars.right + fig.subplotpars.left)/2
            plt.title(f"{subtitle}", color=fg_color2, size=14)
            plt.suptitle(f"{title}", color=fg_color, size=18, x=mid)
        else:
            plt.title(f"{title}", color=fg_color, size=18)
    if xlabel:
        if logx:
            plt.xscale('log')
            plt.xlabel(f'Log {xlabel}', color=fg_color)
        else:
            plt.xlabel(xlabel, color=fg_color)
    if ylabel:
        if logy:
            plt.yscale('log')
            # ax.yaxis.set_major_formatter(ticker.FuncFormatter(myLogFormat))
            plt.ylabel(f'Log {ylabel}', color=fg_color)
        else:
            plt.ylabel(ylabel, color=fg_color)
    svgdirname = dirname + "-svg" 
    try:
        os.mkdir(dirname)
        os.mkdir(svgdirname)
    except FileExistsError:
        pass
    plt.savefig(f"{dirname}/{name}.png")
    plt.savefig(f"{svgdirname}/{name}.svg", format='svg')
    plt.clf()
    plt.close()

def manyLines(
    x_list,
    y_lists,
    y_labels=None,
    title=None,
    subtitle=None,
    xlabel=None,
    ylabel=None,
    logx=False,
    logy=False,
    xrange=None, #Tuple
    yrange=None, #Tuple
    legend_pos=0,
    size=10,
    name="temp_filename",
    dirname="figs",
):
    x_len = len(x_list)
    for y_list in y_lists:
        if len(y_list) != x_len:
            print(
                f"Array size mismatch in {title}"
                + f"\ny len {len(y_list)} != {x_len}"
            )

    alpha = 0.8
    if len(y_lists) > 1:
        alpha = 0.3
    fig, ax = plt.subplots(1, 1, figsize=(10, 5), dpi=300)
    # Set up Axis Definition
    min_x = min(x_list)
    max_x = max(x_list)
    min_y = min([min(y_list) for y_list in y_lists])
    max_y = max([max(y_list) for y_list in y_lists]) 
    max_y = max_y + (max_y - min_y)*0.05 # 5% vertical buffer
    if (xrange):
        min_x = xrange[0]
        max_x = xrange[1]
    if (yrange):
        min_y = yrange[0]
        max_y = yrange[1]
    ax.axis([
        min_x,
        max_x,
        min_y,
        max_y])
    fg_color = 'black'
    fg_color2 = '#1a1a1a'
    bg_color='white'
    ax.patch.set_facecolor(bg_color)
    ax.tick_params(color=fg_color, labelcolor=fg_color)
    for spine in ax.spines.values():
        spine.set_edgecolor(fg_color)
    fig.patch.set_facecolor(bg_color)
    ax.grid(
        visible=True,
        alpha=0.2,
        color=fg_color2,
        linewidth=0.5,
    )
    
    if y_labels == None:
        for i, y_list in enumerate(y_lists):
            ax.plot(
                x_list,
                y_list,
                color="black",
                alpha=alpha,
                # edgecolor="black",
                linewidth=1,
            )
    else:
        for i, label in enumerate(y_labels):
            ax.fill_between(
                x_list,
                y_lists[i],
                color="black",
                alpha=alpha,
                # edgecolor="black",
                linewidth=1,
                label=label,
            )
        ax.legend(loc=legend_pos)
    # if len(y_lists) == 1 and label_vals:
    #     for i, x in enumerate(x_list):
    #         text_str = f'{np.round(y_lists[0][i], 2).__float__()}'
    #         flip = 1 # 1 => left side, 0 => right side
    #         if i == 0:
    #             flip = 0 # First label should be right of point
    #         elif i < len(x_list)-1 and i > 0:
    #             if y_list[i] < y_list[i-1]: # Was decreasing, don't put left
    #                 flip = 0
    #         if flip:
    #             x_offset = -1*(len(text_str)+0.5)*size*2
    #         ax.annotate(
    #             text_str,
    #             (x, y_lists[0][i]),
    #             # xytext=(-len(text_str)*size,-0.5*size),
    #             xytext=(x_offset,0),
    #             textcoords="offset pixels",
    #             color=fg_color,
    #             fontsize=8)
    if title:
        if subtitle:
            mid = (fig.subplotpars.right + fig.subplotpars.left)/2
            plt.title(f"{subtitle}", color=fg_color2, size=14)
            plt.suptitle(f"{title}", color=fg_color, size=18, x=mid)
        else:
            plt.title(f"{title}", color=fg_color, size=18)
    if xlabel:
        if logx:
            plt.xscale('log')
            plt.xlabel(f'Log {xlabel}', color=fg_color)
        else:
            plt.xlabel(xlabel, color=fg_color)
    if ylabel:
        if logy:
            plt.yscale('log')
            # ax.yaxis.set_major_formatter(ticker.FuncFormatter(myLogFormat))
            plt.ylabel(f'Log {ylabel}', color=fg_color)
        else:
            plt.ylabel(ylabel, color=fg_color)
    svgdirname = dirname + "-svg" 
    try:
        os.mkdir(dirname)
        os.mkdir(svgdirname)
    except FileExistsError:
        pass
    plt.savefig(f"{dirname}/{name}.png")
    plt.savefig(f"{svgdirname}/{name}.svg", format='svg')
    plt.clf()
    plt.close()

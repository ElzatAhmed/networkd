import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from random import random

from networkd.classes.networks import DisNet


def plot(
        network: DisNet, pos=None, node_color=None,
        edge_color=None, save_path=None
):
    if edge_color is None:
        edge_color = [(0, 0, 1)]
    if node_color is None:
        node_color = [(0, 1, 0)]
    graph = network.xGraph
    pos = _random_pos(graph) if pos is None else pos
    figure = plt.figure()
    nx.draw_networkx_nodes(G=graph, pos=pos, node_size=5, node_color=node_color)
    nx.draw_networkx_edges(G=graph, pos=pos, width=0.5, edge_color=edge_color)
    if save_path is None:
        plt.show()
    else:
        matplotlib.use("Agg")
        figure.savefig(save_path)


def _random_pos(graph: nx.Graph):
    pos = {}
    for node in graph.nodes:
        pos[node] = (random(), random())
    return pos

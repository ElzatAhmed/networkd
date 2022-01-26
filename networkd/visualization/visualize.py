import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from random import random
from pyvis.network import Network as pyNet

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


def toHtml(
        network: DisNet, pos=None, save_path='network.html',
        node_color='blue', show_buttons=False
):
    nodes = network.nodes
    edges = network.edges
    pynet = pyNet(
        height='700px', width='1500px', notebook=True, layout=False, directed=False
    )
    pos = _random_pos(network.xGraph) if pos is None else pos
    for node in nodes:
        pynet.add_node(node, color=node_color, x=pos[node][0], y=pos[node][1])
    for edge in edges:
        pynet.add_edge(source=edge[0], to=edge[1])
    if show_buttons:
        pynet.width = 1000
        pynet.show_buttons()
    pynet.show(save_path)


def _random_pos(graph: nx.Graph):
    pos = {}
    for node in graph.nodes:
        pos[node] = (random(), random())
    return pos

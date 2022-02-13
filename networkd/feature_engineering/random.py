from networkd.classes.networks import TopologicalDisNet
import networkx as nx
from random import random


def _edges(c, n, p):
    edges = []
    for i in range(n):
        if c == i:
            continue
        if random() < p:
            edges.append((c, i))
    return edges


def random_network(n=100, p=0.5):
    network = TopologicalDisNet()
    network.from_nxGraph(nx.erdos_renyi_graph(n, p, seed=1234))
    return network


def random_networks(d=100, n=100, p=0.5):
    networks = []
    for _ in range(d):
        networks.append(random_network(n, p))
    return networks


def random_centralized_network(n=100, high=0.8, low=0.2):
    network = TopologicalDisNet()
    center = int(random() * n)
    for _ in range(n):
        network.add_node_()
    for i in range(n):
        p = high if i == center else low
        edges = _edges(i, n, p)
        for edge in edges:
            network.add_edge_(edge[0], edge[1])
    return network


def random_centralized_networks(d=100, n=100, high=0.8, low=0.2):
    networks = []
    for _ in range(d):
        networks.append(random_centralized_network(n, high, low))
    return networks

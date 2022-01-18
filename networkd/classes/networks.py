import abc
from abc import ABC

import networkx as nx
import numpy as np


class DisNet(ABC):

    """
    abstract class for disintegration networks
    """

    def __init__(self):
        self._nodes = []
        self._node_flag = []
        self._edges = []
        self._edge_flag = []

    def __str__(self):
        return f'DisNet with {self.node_count} nodes and {self.edge_count} edges'

    def kill_node_(self, nid: int):
        if nid > len(self._nodes):
            return
        self._node_flag[nid] = 0
        for i in range(len(self._edges)):
            if nid in self._edges[i]:
                self._edge_flag[i] = 0

    def kill_edge_(self, eid: int):
        if eid > len(self._edges):
            return
        self._edge_flag[eid] = 0

    @property
    def nodes(self) -> list:
        """
        :return: alive nodes as a list
        """
        return [self._nodes[i] for i in range(len(self._nodes)) if self._node_flag[i]]

    @property
    def edges(self) -> list:
        """
        :return: alive edges as a list
        """
        return [self._edges[i] for i in range(len(self._edges)) if self._edge_flag[i]]

    @property
    def adj(self) -> np.ndarray:
        """
        :return: adjacency matrix of the network as numpy array
        """
        return self._adj()

    @property
    def edge_index(self) -> np.ndarray:
        """
        :return: edge_index of the network as numpy array
        """
        return self._edge_index()

    @property
    def con(self) -> np.ndarray:
        """
        :return: connection matrix of the network as numpy array
        """
        return self._con()

    @property
    def node_count(self):
        return len(self.nodes)

    @property
    def edge_count(self):
        return len(self.edges)

    @property
    def xGraph(self) -> nx.Graph:
        """
        :return: construct identical networkx graph
        """
        graph = nx.Graph()
        graph.add_nodes_from(self.nodes)
        graph.add_edges_from(self.edges)
        return graph

    def _adj(self):
        adj = np.zeros(shape=(self.node_count, self.node_count), dtype=np.int64)
        for edge in self.edges:
            adj[edge[0]][edge[1]] = 1
        return adj

    def _edge_index(self):
        e1 = []
        e2 = []
        for edge in self.edges:
            e1.append(edge[0])
            e2.append(edge[1])
        return np.asarray([e1, e2], dtype=np.int64)

    def _con(self):
        paths = dict(nx.all_pairs_shortest_path(self.xGraph))
        con = np.zeros(shape=(self.node_count, self.node_count), dtype=np.int64)
        for i in paths:
            for j in paths[i]:
                con[i][j] = 1
        return con

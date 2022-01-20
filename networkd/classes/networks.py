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

        """
        killing the node with given id and the corresponding edges
        :param nid: node id
        :return:
        """

        if nid > len(self._nodes):
            return
        self._node_flag[nid] = 0
        for i in range(len(self._edges)):
            if nid in self._edges[i]:
                self._edge_flag[i] = 0

    def kill_edge_(self, eid: int):

        """
        killing the edge with the given id
        :param eid: edge id
        :return:
        """

        if eid > len(self._edges):
            return
        self._edge_flag[eid] = 0

    @abc.abstractmethod
    def add_node_(self, node, **attr):
        pass

    @abc.abstractmethod
    def add_edge_(self, n1, n2, **attr):
        pass

    @abc.abstractmethod
    def from_nxGraph(self, graph: nx.Graph):
        pass

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
        adj = np.zeros(shape=(len(self._nodes), len(self._nodes)), dtype=np.int64)
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
        con = np.zeros(shape=(len(self._nodes), len(self._nodes)), dtype=np.int64)
        for i in paths:
            for j in paths[i]:
                con[i][j] = 1
        return con


class TopologicalDisNet(DisNet):

    """
    Topological disintegration network
    """

    def __init__(self):
        super(TopologicalDisNet, self).__init__()

    def add_node_(self, node, **attr):
        if node in self._nodes:
            nid = self._nodes.index(node)
            if self._node_flag[nid]:
                raise Exception(f'disnet contains a same node: {node}')
            else:
                self._node_flag[nid] = 1
                return
        self._nodes.append(node)
        self._node_flag.append(1)

    def add_edge_(self, n1, n2, **attr):
        if n1 in self.nodes and n2 in self.nodes:
            self._edges.append((n1, n2))
            self._edge_flag.append(1)
            return
        raise Exception('n1 or n2 is not a node in disnet')

    def from_nxGraph(self, graph: nx.Graph):
        self._nodes.clear()
        self._edges.clear()
        for node in graph.nodes:
            self.add_node_(node)
        for edge in graph.edges:
            self.add_edge_(edge[0], edge[1])

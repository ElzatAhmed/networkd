import abc

from networkd.classes import DisNet
import networkx as nx
import numpy as np
from abc import ABC


class _Centrality(ABC):

    """
    an abstract super class for centrality methods
    """

    def __init__(self, network: DisNet):
        self._network = network

    @abc.abstractmethod
    def _dictionary(self) -> dict:
        pass

    def _sorted(self, reverse=True) -> list:
        dic = self._dictionary()
        sort = sorted(dic.items(), key=lambda x: x[1], reverse=reverse)
        if len(sort) == 0:
            return []
        return [s[0] for s in sort]

    @property
    def dictionary(self):
        return self._dictionary()

    @property
    def ascending(self):
        return self._sorted(reverse=False)

    @property
    def descending(self):
        return self._sorted()

    def minimum(self) -> list:
        values = self._sorted(reverse=False)
        if len(values) > 0:
            if type(values[0]) is list:
                return values[0]
            return [values[0]]
        return []

    def maximum(self) -> list:
        values = self._sorted()
        if len(values) > 0:
            if type(values[0]) is list:
                return values[0]
            return [values[0]]
        return []

    def mean(self) -> list:
        # TODO: implementation
        values = list(self.dictionary.items())
        mean = np.mean(values)
        return list()

    @property
    def network(self) -> DisNet:
        return self._network


class NodeCentrality(_Centrality, ABC):

    """
    an abstract super class for node centrality methods
    """

    def __init__(self, network: DisNet):
        super(NodeCentrality, self).__init__(network)


class EdgeCentrality(_Centrality, ABC):

    """
    an abstract super class for edge centrality methods
    """

    def __init__(self, network: DisNet):
        super(EdgeCentrality, self).__init__(network)


class DegreeCentrality(NodeCentrality):

    def __init__(self, network: DisNet):
        super(DegreeCentrality, self).__init__(network)

    def _dictionary(self):
        return nx.degree_centrality(G=self._network.xGraph)


class BetweennessCentrality(NodeCentrality):

    def __init__(self, network: DisNet):
        super(BetweennessCentrality, self).__init__(network)

    def _dictionary(self):
        return nx.betweenness_centrality(G=self._network.xGraph)


class SemiLocalCentrality(NodeCentrality):

    def __init__(self, network: DisNet):
        super(SemiLocalCentrality, self).__init__(network)

    def _dictionary(self):
        return self._semi_local()

    def _semi_local(self):
        adj = self._network.adj
        semi_local = {}
        nodes = self._network.nodes
        for node in nodes:
            value = 0
            for i in range(len(adj[node])):
                neighbor = adj[node][i]
                if neighbor:
                    value += sum(adj[i])
            semi_local[node] = value
        return semi_local


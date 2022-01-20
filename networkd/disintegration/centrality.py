import abc

from networkd.classes import DisNet
import networkx as nx
from abc import ABC


class Centrality(ABC):
    """
    an abstract super class for centrality methods
    """

    def __init__(self, network: DisNet):
        self._network = network

    @abc.abstractmethod
    def dict_value(self) -> dict:
        """
        :return: a dict with node as key centrality value as value
        """
        pass

    @property
    def sorted_value(self) -> list:
        """
        :return: a list of node sorted with centrality value
        """
        dic = self.dict_value
        sort = sorted(dic.items(), key=lambda x: x[1], reverse=True)
        if len(sort) == 0:
            return []
        return [s[0] for s in sort]

    @property
    def max_node(self):
        """
        :return: a list of nodes with the max centrality value
        """
        values = self.sorted_value
        return [values[0]] if len(values) > 0 else None


class DegreeCentrality(Centrality):

    def __init__(self, network: DisNet):
        super(DegreeCentrality, self).__init__(network)

    @property
    def dict_value(self):
        return nx.degree_centrality(G=self._network.xGraph)


class BetweennessCentrality(Centrality):

    def __init__(self, network: DisNet):
        super(BetweennessCentrality, self).__init__(network)

    @property
    def dict_value(self):
        return nx.betweenness_centrality(G=self._network.xGraph)


class SemiLocalCentrality(Centrality):

    def __init__(self, network: DisNet):
        super(SemiLocalCentrality, self).__init__(network)

    @property
    def dict_value(self):
        return dict()

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
    def value(self) -> dict:
        """
        :return: centrality value
        """
        pass


class DegreeCentrality(Centrality):

    def __init__(self, network: DisNet):
        super(DegreeCentrality, self).__init__(network)

    @property
    def value(self):
        return nx.degree_centrality(G=self._network.xGraph)


class BetweennessCentrality(Centrality):

    def __init__(self, network: DisNet):
        super(BetweennessCentrality, self).__init__(network)

    @property
    def value(self):
        return nx.betweenness_centrality(G=self._network.xGraph)

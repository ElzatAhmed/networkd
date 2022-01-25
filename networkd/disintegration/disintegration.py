import abc
from abc import ABC

from networkd.classes import DisNet
from networkd.disintegration import NodeCentrality, EdgeCentrality

_strategies = ['max', 'min', 'mean']


class Disintegration(ABC):

    """
    an abstract super class for disintegration methods
    needs a callable centrality method and a network as type DisNet
    """

    def __init__(self, centrality, strategy: str):
        if strategy not in _strategies:
            raise Exception(f'strategy must be one of {str(_strategies)}')
        self._centrality = centrality
        self._network = centrality.network
        self._strategy = strategy
        self._dict = {
            'max': self._centrality.maximum,
            'min': self._centrality.minimum,
            'mean': self._centrality.mean
        }

    @abc.abstractmethod
    def disintegrate(self, cost) -> DisNet:
        pass


class NodeDisintegration(Disintegration):

    def __init__(self, centrality: NodeCentrality, strategy: str):
        super(NodeDisintegration, self).__init__(centrality, strategy)

    def disintegrate(self, cost) -> DisNet:
        return self._disintegrate(cost)

    def _disintegrate(self, cost):
        if cost < 0:
            raise Exception("cost must be greater than 0")
        if cost > len(self._network.nodes):
            for node in self._network.nodes:
                self._network.kill_node_(node)
            return self._network
        while True:
            nodes = self._dict[self._strategy]()
            for node in nodes:
                self._network.kill_node_(node)
                cost -= 1
                if cost <= 0:
                    break
            if cost <= 0:
                break
        return self._network


class EdgeDisintegration(Disintegration):

    def __init__(self, centrality: EdgeCentrality, strategy: str):
        super(EdgeDisintegration, self).__init__(centrality, strategy)

    def disintegrate(self, cost) -> DisNet:
        return self._disintegrate(cost)

    def _disintegrate(self, cost):
        if cost < 0:
            raise Exception("cost must be greater than 0")
        if cost > len(self._network.edges):
            for edge in self._network.edges:
                self._network.kill_edge_(edge)
            return self._network
        while True:
            edges = self._dict[self._strategy]()
            for edge in edges:
                self._network.kill_edge_(edge)
                cost -= 1
                if cost <= 0:
                    break
            if cost <= 0:
                break
        return self._network

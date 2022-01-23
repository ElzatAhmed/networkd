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

    @abc.abstractmethod
    def disintegrate(self, cost) -> DisNet:
        pass


class NodeDisintegration(Disintegration):

    def __init__(self, centrality: NodeCentrality, strategy: str):
        super(NodeDisintegration, self).__init__(centrality, strategy)

    def disintegrate(self, cost) -> DisNet:
        pass


class EdgeDisintegration(Disintegration):

    def __init__(self, centrality: EdgeCentrality, strategy: str):
        super(EdgeDisintegration, self).__init__(centrality, strategy)

    def disintegrate(self, cost) -> DisNet:
        pass

from networkd.classes import TopologicalDisNet
from networkd.disintegration import *
from .random import random_centralized_network
import numpy as np
import json


centrality = {
    'degree': DegreeCentrality,
    'betweenness': BetweennessCentrality,
    'semi_local': SemiLocalCentrality
}


class NodeDisintegrationFeatureData:

    def __init__(self, size):
        self._size = size
        self._labels = {
            'degree': None,
            'betweenness': None,
            'semi_local': None
        }
        self._network = None

    def generate(self):
        self._network = random_centralized_network(n=self._size, high=0.9, low=0.05)
        for key in centrality:
            cen = centrality[key](self._network)
            label = cen.maximum()
            self._labels[key] = label

    @property
    def network_size(self):
        return self._size

    @property
    def network(self):
        return self._network

    @property
    def degree_label(self):
        return self._labels['degree']

    @property
    def betweenness_label(self):
        return self._labels['betweenness']

    @property
    def semiLocal_label(self):
        return self._labels['semi_local']

    @property
    def dict(self):
        return {
            'size': self._size,
            'labels': self._labels,
            'network': self._network.dict()
        }

    @property
    def json(self):
        return json.dumps(self.dict, indent=2)

    @staticmethod
    def from_json(json_file):
        json_obj = json.load(json_file)
        data = NodeDisintegrationFeatureData(size=int(json_obj['size']))
        data._labels = json_obj['labels']
        data._network = TopologicalDisNet()
        data._network.from_json(source=json_obj['network'])
        return data

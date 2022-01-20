from networkd.classes import DisNet


class Disintegration:

    def __init__(self, centrality: callable, network: DisNet):
        self._centrality = centrality(network)
        self._network = network

    def disintegrate(self, cost):
        while cost > 0:
            nodes = self._centrality.max_node
            if len(nodes) <= cost:
                cost -= len(nodes)
                for node in nodes:
                    self._network.kill_node_(node)
            else:
                for i in range(cost):
                    self._network.kill_node_(nodes[i])
                break
        return self._network

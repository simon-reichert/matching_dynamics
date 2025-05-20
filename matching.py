import networkx as nx

class Network():
    """
    A class which represents a social network consisting of social links and possible matching edges and the actual matching.
    These are split into three graphs. The graph with the matching edges has a benefit for every edge.

    """
    def __init__(self):
        self.links = nx.Graph()
        self.potential = nx.Graph()
        self.matching = nx.Graph()
        self._discovery = nx.Graph()


    def add_link(self, u,v):
        self.links.add_edge(u,v)
        self.matching.add_nodes_from([u,v])
        self.potential.add_nodes_from([u,v])
        self._update_discovery()

    def add_links(self, list):
        self.links.add_edges_from(list)
        self._update_discovery()
    
    def add_matching_edge(self, u,v,**attr):
        self.potential.add_edge(u, v, **attr)
        self.matching.add_nodes_from([u,v])
        self.links.add_nodes_from([u,v])

    def add_matching_edges(self, list):
        self.potential.add_edges_from(list)

    def draw(self, pos):
        width = 3
        nx.draw_networkx_nodes(self.links, pos=pos, node_size=500)
        nx.draw_networkx_labels(self.links, pos=pos)
        nx.draw_networkx_edges(self.links, pos=pos, edge_color="gray", width=width)
        nx.draw_networkx_edges(self.potential, pos=pos, width=width)
        nx.draw_networkx_edges(self.matching, pos = pos, width=width, edge_color="r")
        labels=  {(e[0],e[1]) :e[2] for e in self.potential.edges.data("b")}
        p =nx.draw_networkx_edge_labels(self.potential, pos=pos, edge_labels=labels)

    def iterate(self):
        steps = 0
        while True:
            if not self.best_step(False):
                break
            steps +=1
        return steps 

    def best_step(self, verbose:bool=True):
        """
        Does a best improvement move 
        """
        best = 0
        edge = None
        for n in self.links.nodes:
            b, e = self.best_step_node(n)
            if b > best:
                best = b
                edge = e
        if best == 0:
            if verbose:
                print("no improvement possible")
            return False
        
        self.remove_matching_edge(edge[0])
        self.remove_matching_edge(edge[1])
        self.matching.add_edge(*edge, b=best)
        if verbose:
            print(f"Added edge {edge}")
        self._update_discovery()
        return True

    
    def best_step_node(self, node):
        """
        Finds best improvement move for given node (in 2 neighborhood)
        """
        blocking_edges = self.get_visible_blocking_edges(node)
        if len(blocking_edges) == 0:
            return 0, None
        best = max(blocking_edges, key=lambda p:blocking_edges.get(p).get("b"))
        new_benefit = self.potential.edges[node, best]["b"]
        return new_benefit, (node, best)

    def get_visible_blocking_edges(self, node):
        T = nx.bfs_tree(self._discovery, node, depth_limit=2)
        visible_edges = nx.subgraph(self.potential, T.nodes)[node]
        blocking_edges = {}
        for key, value in visible_edges.items():
            if self.current_benefit(key) < value["b"] and self.current_benefit(node)  < value["b"]:
                blocking_edges[key] = value
        return blocking_edges

    def current_benefit(self, node):
        m = self.matching[node]
        if len(m) == 0:
            return 0
        return list(m.values())[0]["b"]

    def is_matched(self, node):
        return not len(self.matching[node]) == 0

    def remove_matching_edge(self, node):
        if self.is_matched(node):
            vertex = next(iter(self.matching[node].keys()))
            self.matching.remove_edge(node, vertex)

    def has_blocking_pair(self):
        """
        Return if there is any blocking pair in the graph
        """

    def _update_discovery(self):
        self._discovery = nx.compose(self.matching, self.links)
        
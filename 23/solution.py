from typing import Self
import networkx as nx

class Node:
    def __init__(self, name:str):
        self.name = name
        self.neighbors: set[Self] = set()

graph: dict[str, Node] = dict()
edge_list = list()

with open('input.txt') as file:
    for line in file:
        edge = line.rstrip('\n').split('-')
        for name in edge:
            if name not in graph:
                graph[name] = Node(name)
        graph[edge[0]].neighbors.add(graph[edge[1]])
        graph[edge[1]].neighbors.add(graph[edge[0]])
        edge_list.append(edge)

triplet_subgraphs: set[frozenset[str]] = set()
t_prefixed_count = 0

for node in graph.values():
    for neighbor in node.neighbors:
        for tri_neighbor in [n for n in neighbor.neighbors if n.name != node.name]:
            if tri_neighbor in node.neighbors:
                triplet = frozenset([node.name, neighbor.name, tri_neighbor.name])
                if triplet not in triplet_subgraphs:
                    triplet_subgraphs.add(triplet)
                    if any(name.startswith('t') for name in triplet):
                        t_prefixed_count += 1

graph = nx.Graph(edge_list)
max_clique = max(nx.algorithms.clique.find_cliques(graph), key = len)
max_clique.sort()

print('Part 1: ', t_prefixed_count)
print('Part 2: ', ','.join(max_clique))

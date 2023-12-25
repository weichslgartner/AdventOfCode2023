from collections import defaultdict
from math import prod

import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import kernighan_lin_bisection

from aoc import get_lines

def draw_graph(graph_dict):
    # Create a directed graph from the dictionary
    G = nx.DiGraph(graph_dict)

    # Draw the graph
    pos = nx.spring_layout(G)  # You can choose a different layout if needed
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', arrowsize=15)

    # Display the graph
    plt.show()

def parse_input(lines):
    graph = defaultdict(list)
    for line in lines:
        src, dst = line.split(":",1)
        graph[src] += dst.split()
        for n in graph[src]:
            graph[n].append(src)
   # draw_graph(graph)

    return nx.Graph(graph)


def part_1(graph: nx.Graph):
    #draw_graph(graph)
    remove_real_input_edges(graph)
    # draw_graph(graph)
    comps = list(nx.connected_components(graph))
    #print(comps)
    #res = kernighan_lin_bisection(graph, partition=None, max_iter=10, weight=None, seed=None)
    #print(res)
    return prod(map(len,comps))


def remove_example_edges(graph):
    graph.remove_edge("hfx", "pzl")
    graph.remove_edge("bvb", "cmg")
    graph.remove_edge("nvd", "jqt")

def remove_real_input_edges(graph):
    graph.remove_edge("fts", "nvb")
    graph.remove_edge("qmr", "kzx")
    graph.remove_edge("zns", "jff")

def part_2(lines):
    pass


def main():
    lines = get_lines("input_25.txt")
    graph = parse_input(lines)
    print("Part 1:", part_1(graph))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()

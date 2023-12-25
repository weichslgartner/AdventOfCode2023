from collections import defaultdict
from math import prod
from typing import List

import networkx as nx
import matplotlib.pyplot as plt
from networkx import minimum_edge_cut

from aoc import get_lines


def draw_graph(graph: nx.Graph) -> None:
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', arrowsize=15)
    plt.show()


def parse_input(lines: List[str]) -> nx.Graph:
    graph = defaultdict(list)
    for line in lines:
        src, dst = line.split(":", 1)
        graph[src] += dst.split()
    return nx.Graph(graph)


def part_1(graph: nx.Graph) -> int:
    graph.remove_edges_from(minimum_edge_cut(graph))
    return prod(map(len, nx.connected_components(graph)))


def part_2(_):
    pass


def main():
    lines = get_lines("input_25.txt")
    graph = parse_input(lines)
    print("Part 1:", part_1(graph))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()

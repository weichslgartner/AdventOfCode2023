from collections import namedtuple
from math import lcm
from typing import Dict, Tuple

from aoc import input_as_str
import re


class Node(namedtuple('Node', 'name left right')):
    def __repr__(self) -> str:
        return f'{self.name} {self.left} {self.right}'


def parse_input(input_str: str) -> Tuple[str, Dict[str, Node]]:
    directions, nodes_raw = input_str.split("\n\n", 1)
    node_dict = {}
    for node_raw in nodes_raw.split("\n"):
        matches = re.findall(r'[1-9A-Z]+', node_raw)
        node = Node(*matches)
        node_dict[node.name] = node
    return directions, node_dict


def part_1(directions: str, node_dict: Dict[str, Node]) -> int:
    return calc_steps(node_dict['AAA'], directions, node_dict, 'ZZZ')


def part_2(directions: str, node_dict: Dict[str, Node]) -> int:
    cur = (node_dict[k] for k in node_dict.keys() if k.endswith('A'))
    return lcm(*[calc_steps(c, directions, node_dict) for c in cur])


def calc_steps(cur: Node, directions: str, node_dict: Dict[str, Node], end_pattern: str = 'Z') -> int:
    steps = 0
    while not cur.name.endswith(end_pattern):
        for d in directions:
            if d == 'L':
                cur = node_dict[cur.left]
            else:
                cur = node_dict[cur.right]
            steps += 1
    return steps


def main():
    lines = input_as_str("input_08.txt")
    directions, node_dict = parse_input(lines)
    print("Part 1:", part_1(directions, node_dict))
    print("Part 2:", part_2(directions, node_dict))


if __name__ == '__main__':
    main()

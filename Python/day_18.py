import sys
from collections import namedtuple, deque
from enum import Enum, StrEnum
from typing import List

from aoc import get_lines, Point, get_neighbours_4


class Dir(StrEnum):
    RIGHT = 'R'
    DOWN = 'D'
    LEFT = 'L'
    UP = 'U'


def dir_to_point(direction: Dir) -> Point:
    if direction == Dir.RIGHT:
        return Point(1, 0)
    if direction == Dir.LEFT:
        return Point(-1, 0)
    if direction == Dir.DOWN:
        return Point(0, 1)
    if direction == Dir.UP:
        return Point(0, -1)


hex_to_dir = {'0': Dir.RIGHT, '1': Dir.DOWN, '2': Dir.LEFT, '3': Dir.UP}


class Trench(namedtuple('Element', 'dir len')):
    def __repr__(self):
        return f'{self.dir} {self.len}'


def parse_input(lines: List[str]) -> List[Trench]:
    trenches = []
    perim = 0
    for line in lines:
        direct, len, color = line.split(' ', 3)
        trenches.append((Trench(Dir(direct), int(len)), Trench(Dir(hex_to_dir[color[-2]]), int(color[2:-2], 16))))
        perim += int(len)
    return trenches


def part_1(trenches):
    return solve([t for t, _ in trenches])


def part_2(trenches):
    return solve([t for _, t in trenches])


def solve(trenches):
    perim, polygon = create_polygon(trenches)
    return calc_area(polygon, perim)


def create_polygon(trenches):
    start = Point(0, 0)
    polygon = [start]
    perim = 0
    for trench in trenches:
        l = polygon[-1]
        perim += trench.len
        dp = dir_to_point(trench.dir)
        polygon.append(Point(l.x + dp.x * trench.len, l.y + dp.y * trench.len))
    return perim, polygon


def calc_area(polygon, perim):
    area = 0
    for p1, p2 in zip(polygon, polygon[1:]):
        area += (p1.x * p2.y - p1.y * p2.x)
    return ((area + perim) // 2) + 1


def main():
    lines = get_lines("input_18.txt")
    trenches = parse_input(lines)
    print("Part 1:", part_1(trenches))
    print("Part 2:", part_2(trenches))


if __name__ == '__main__':
    main()

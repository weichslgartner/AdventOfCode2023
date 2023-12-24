from dataclasses import dataclass
from typing import Set

from aoc import get_lines, Point, dir_to_point, get_neighbours_4

@dataclass
class Element:
    p: Point
    visited: Set[Point]

def parse_input(lines):
    rocks = set()
    slopes = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                rocks.add(Point(x, y))
            if c in '<>v^':
                slopes[Point(x, y)] = c
    return rocks, slopes, Point(len(lines[0]), len(lines))

def part_1(rocks, slopes, max_p, part1=False):
    queue = [Element(p=Point(1,0),visited=set())]
    visited_map = {}
    longest_path = 0
    while len(queue) > 0:
        el = queue.pop()
        el.visited.add(el.p)
        visited_map[el.p] = len(el.visited)
        if el.p.x == max_p.x-2 and el.p.y == max_p.y-1:
            longest_path=max(longest_path,len(el.visited))
        if el.p in slopes and part1:
            diff_p = dir_to_point(slopes[el.p])
            el.p= Point(el.p.x+diff_p.x,el.p.y+diff_p.y)
            if el.p not in el.visited:
                queue.append(el)
            continue
        for n in get_neighbours_4(el.p,max_p):
            if n not in el.visited and n not in rocks and (n not in visited_map or len(el.visited) >= visited_map[n]-1):
                el_n = Element(n,el.visited.copy())
                queue.append(el_n)
    return longest_path-1

def part_2(lines):
    pass


def main():
    lines = get_lines("input_23_test.txt")
    rocks, slopes, max_p = parse_input(lines)
    print("Part 1:", part_1(rocks, slopes, max_p))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()

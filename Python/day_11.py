from itertools import combinations
from typing import Set, Tuple, List

from aoc import get_lines, Point, manhattan_distance


def parse_input(lines: List[str]) -> Tuple[Set[Point], Point]:
    point2galaxy = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != '.':
                point2galaxy.add(Point(x, y))
    return point2galaxy, Point(len(lines[0]), len(lines))


def expand_universe(pmax: Point, point2galaxy: Set[Point], expand_times: int = 2) -> Set[Point]:
    to_add = expand_times - 1
    y_expand = [y for y in range(pmax.y) if all(Point(x, y) not in point2galaxy for x in range(pmax.x))]
    x_expand = [x for x in range(pmax.x) if all(Point(x, y) not in point2galaxy for y in range(pmax.y))]
    for i, y_plus in enumerate(y_expand):
        for p in list(point2galaxy):
            if p.y > y_plus + i * to_add:
                point2galaxy.add(Point(p.x, p.y + to_add))
                point2galaxy.remove(p)
    for i, x_plus in enumerate(x_expand):
        for p in list(point2galaxy):
            if p.x > x_plus + i * to_add:
                point2galaxy.add(Point(p.x + to_add, p.y))
                point2galaxy.remove(p)
    return point2galaxy


def calc_sum_shortest_paths(point2galaxy: Set[Point]) -> int:
    return sum(manhattan_distance(i, j) for i, j in combinations(point2galaxy, 2))


def part_1(point2galaxy: Set[Point], pmax: Point) -> int:
    return calc_sum_shortest_paths(expand_universe(pmax, point2galaxy))


def part_2(point2galaxy: Set[Point], pmax: Point) -> int:
    return calc_sum_shortest_paths(expand_universe(pmax, point2galaxy, expand_times=1000000))


def main() -> None:
    lines = get_lines("input_11.txt")
    point2galaxy, pmax = parse_input(lines)
    print("Part 1:", part_1(point2galaxy.copy(), pmax))
    print("Part 2:", part_2(point2galaxy, pmax))


if __name__ == '__main__':
    main()

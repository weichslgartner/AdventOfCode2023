from collections import namedtuple
from enum import StrEnum
from functools import reduce
from typing import List, Tuple

from aoc import get_lines, Point


class Dir(StrEnum):
    RIGHT = 'R'
    DOWN = 'D'
    LEFT = 'L'
    UP = 'U'


dir_2_point = {
    Dir.RIGHT: Point(1, 0),
    Dir.LEFT: Point(-1, 0),
    Dir.DOWN: Point(0, 1),
    Dir.UP: Point(0, -1),
}

hex_to_dir = {'0': Dir.RIGHT, '1': Dir.DOWN, '2': Dir.LEFT, '3': Dir.UP}


class Trench(namedtuple('Trench', 'dir len')):
    def __repr__(self) -> str:
        return f'{self.dir} {self.len}'


def parse_input(lines: List[str]) -> List[Tuple[Trench, Trench]]:
    return [(Trench(Dir(d), int(l)), Trench(Dir(hex_to_dir[c[-2]]), int(c[2:-2], 16))) for d, l, c in
            map(lambda line: line.split(' ', 3), lines)]


def create_polygon(trenches: List[Trench]) -> Tuple[int, List[Point]]:
    return reduce(
        lambda acc, trench: (
            acc[0] + trench.len,
            acc[1] + [Point(acc[1][-1].x + dir_2_point[trench.dir].x * trench.len,
                            acc[1][-1].y + dir_2_point[trench.dir].y * trench.len)],
        ),
        trenches,
        (0, [Point(0, 0)])
    )


def calc_area(perim: int, polygon: List[Point]) -> int:
    return (sum(p1.x * p2.y - p1.y * p2.x for p1, p2 in zip(polygon, polygon[1:])) + perim) // 2 + 1


def solve(trenches: List[Trench]) -> int:
    return calc_area(*create_polygon(trenches))


def part_1(trenches: List[Trench]) -> int:
    return solve([t for t, _ in trenches])


def part_2(trenches: List[Trench]) -> int:
    return solve([t for _, t in trenches])


def main() -> None:
    lines: List[str] = get_lines("input_18.txt")
    trenches: List[Tuple[Trench, Trench]] = parse_input(lines)
    print("Part 1:", part_1(trenches))
    print("Part 2:", part_2(trenches))


if __name__ == '__main__':
    main()

from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple

from aoc import get_lines

from math import prod, sqrt, ceil, floor


@dataclass
class Race:
    time: float
    distance: float

    @classmethod
    def from_str(cls, t: str, d: str) -> 'Race':
        return cls(float(t), float(d))


def parse_input(lines: List[str]) -> Tuple[List[Race], List[Race]]:
    t_d = list(zip(*(line.split(':', 1)[1].split() for line in lines)))
    races = [Race.from_str(t, d) for t, d in t_d]
    races2 = [Race.from_str(*reduce(lambda acc, x: (acc[0] + x[0], acc[1] + x[1]), t_d, ("", "")))]
    return races, races2


def solve(races: List[Race]) -> int:
    return prod(map(solve_quadratic_eq, races))


def solve_quadratic_eq(race: Race) -> int:
    discriminant = race.time ** 2 - 4.0 * race.distance
    solution1 = (-race.time + sqrt(discriminant)) / (-2.0)
    solution2 = (-race.time - sqrt(discriminant)) / (-2.0)
    return int((ceil(solution2 - 1.0) - floor(solution1 + 1.0)) + 1)


def part_1(races: List[Race]) -> int:
    return solve(races)


def part_2(races: List[Race]) -> int:
    return solve(races)


def main():
    lines = get_lines("input_06.txt")
    races, races2 = parse_input(lines)
    print("Part 1:", part_1(races))
    print("Part 2:", part_2(races2))


if __name__ == '__main__':
    main()

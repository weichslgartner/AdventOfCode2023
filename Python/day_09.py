from functools import reduce

from typing import List, Any
from aoc import get_lines, extract_all_ints


def parse_input(lines: List[str]) -> List[List[int]]:
    return [extract_all_ints(l) for l in lines]


def part_1(oasis: List[List[int]]) -> int:
    return sum(reduce(lambda accu, h: accu + h[-1], calc_history(o), 0) for o in oasis)


def part_2(oasis: List[List[int]]) -> int:
    return sum(reduce(lambda accu, h: h[0] - accu, reversed(calc_history(o)), 0) for o in oasis)


def calc_history(cur: List[int]) -> List[List[int]]:
    history = [cur]
    while not all(c == 0 for c in cur):
        cur = [j - i for i, j in zip(cur, cur[1:])]
        history.append(cur)
    return history


def main() -> None:
    lines = get_lines("input_09.txt")
    oasis = parse_input(lines)
    print("Part 1:", part_1(oasis))
    print("Part 2:", part_2(oasis))


if __name__ == '__main__':
    main()

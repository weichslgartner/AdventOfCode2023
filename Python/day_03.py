from math import prod
from typing import List, Dict, Set

from aoc import get_lines, Point


def parse_input(lines: List[str]) -> (Dict, Dict):
    num = ""
    p = None
    nums = {}
    symbols = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c.isdigit():
                if len(num) == 0:
                    p = Point(x=x, y=y)
                num += c
            elif c == '.':
                if len(num) != 0:
                    nums[p] = num
                    num = ""
            else:
                if len(num) != 0:
                    nums[p] = num
                    num = ""
                symbols[Point(x=x, y=y)] = c
    return nums, symbols


def has_sym_neighbor(p: Point, length: int, symbols) -> bool:
    for y in range(p.y - 1, p.y + 2):
        for x in range(p.x - 1, p.x + length + 1):
            if Point(x, y) in symbols:
                return True
    return False


def part_1(nums: Dict[Point, str], symbols: Set[Point]) -> int:
    return sum(int(numb) for _, numb in filter(lambda x: has_sym_neighbor(x[0], len(x[1]), symbols), nums.items()))


def get_gear(p: Point, nums: Dict[Point, str]) -> int:
    gear = set()
    for y in range(p.y - 1, p.y + 2):
        for x in range(p.x - 1, p.x + 2):
            n = Point(x, y)
            if n in nums:
                gear.add(int(nums[n]))
    return prod(gear) if len(gear) == 2 else 0


def part_2(nums: Dict[Point, str], symbols_dict: Dict[Point, str]) -> int:
    return sum(get_gear(p, expand_nums(nums)) for p, _ in filter(lambda x: x[1] == "*", symbols_dict.items()))


def expand_nums(nums):
    nums2 = {}
    for p, v in nums.items():
        for i in range(len(v)):
            nums2[Point(x=p.x + i, y=p.y)] = v
    return nums2


def main():
    lines = get_lines("input_03.txt")
    nums, symbols_dict = parse_input(lines)
    print("Part 1:", part_1(nums, symbols_dict.keys()))
    print("Part 2:", part_2(nums, symbols_dict))


if __name__ == '__main__':
    main()

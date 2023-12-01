from typing import List, Union

from aoc import get_lines


def part_1(lines: List[str]) -> int:
    agg = 0
    for line in lines:
        digits = [int(i) for i in filter(lambda c: c.isdigit(), line)]
        agg += 10 * digits[0] + digits[-1]
    return agg


def part_2(lines: List[str]) -> int:
    agg = 0
    for line in lines:
        digits = []
        for i, c in enumerate(line):
            if c.isdigit():
                digits.append(int(c))
            elif num := words2num(i, line):
                digits.append(num)
        agg += 10 * digits[0] + digits[-1]
    return agg


def words2num(i: int, line: str) -> Union[int, None]:
    replace_dict = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
                    'eight': 8, 'nine': 9}
    for old, new in replace_dict.items():
        if i + len(old) <= len(line) and line[i:i + len(old)] == old:
            return new
    return None


def main():
    lines = get_lines("input_01.txt")
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()

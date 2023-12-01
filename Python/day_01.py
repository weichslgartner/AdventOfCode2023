from typing import List

from aoc import get_lines


def part_1(lines : List[str]) -> str:
    agg = 0
    for line in lines:
        digits = [int(i) for i in filter(lambda c: c.isdigit(), line)]
        agg += 10 * digits[0] + digits[-1]
    return agg


def part_2(lines : List[str]) -> str:
    replace_dict = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
                    'eight': 8, 'nine': 9}

    agg = 0
    for line in lines:
        digits = []
        for i, c in enumerate(line):
            if c.isdigit():
                digits.append(int(c))
            for old, new in replace_dict.items():
                if i + len(old) <= len(line) and line[i:i + len(old)] == old:
                    digits.append(int(new))
        agg += 10 * digits[0] + digits[-1]
    return agg


def main():
    lines = get_lines("input_01.txt")
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()

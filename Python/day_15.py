from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple

from Python.aoc import input_as_str


@dataclass
class Lens:
    label: str
    focal: int


def aoc_hash(x: str) -> int:
    return reduce(lambda accu, c: (accu + ord(c)) * 17 % 256, x, 0)


def focus_power(vec: List[List[Lens]]) -> int:
    return sum(
        (box_n + 1) * sum((pos + 1) * lenses.focal for pos, lenses in enumerate(content))
        for box_n, content in enumerate(vec)
    )


def part_1(input_str: str) -> int:
    return sum(aoc_hash(part) for part in input_str.split(','))


def part_2(input_str: str) -> int:
    vec = [[] for _ in range(256)]
    for s in input_str.split(','):
        if '=' in s:
            label, focal = s.split('=',1)
            idx = aoc_hash(label)
            lens = Lens(label, int(focal))
            same_label_idx = next((i for i, x in enumerate(vec[idx]) if x.label == lens.label), None)
            if same_label_idx is not None:
                vec[idx][same_label_idx] = lens
            else:
                vec[idx].append(lens)
        else:
            label, _ = s.split('-',1)
            idx = aoc_hash(label)
            same_label_idx = next((i for i, x in enumerate(vec[idx]) if x.label == label), None)
            if same_label_idx is not None:
                vec[idx].pop(same_label_idx)

    return focus_power(vec)


def main():
    input_data = input_as_str("input_15.txt")
    print("Part 1:", part_1(input_data))
    print("Part 2:", part_2(input_data))


if __name__ == '__main__':
    main()

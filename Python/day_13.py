from typing import List

from aoc import get_lines, input_as_str


def transpose(l: List[str]) -> List[str]:
    return [''.join(s) for s in zip(*l)]


def parse_input(lines):
    return [block.split() for block in lines.split("\n\n")]


def part_1(blocks):
    # print(blocks)
    sum = 0
    for block in blocks:
        if i := reflection_size(block):
            sum += 100 * i
        else:
            tr_block = transpose(block)
            if i := reflection_size(tr_block):
                sum += i
            else:
                print('\n'.join(block))
                print()
    return sum


def reflection_size(block):
    same_id = possible_splits(block)

    if len(same_id) == 0:
        return None
    for s in same_id:
        l1_idx = s
        l2_idx = s + 1
        i = 0
        while l1_idx >= 0 and l2_idx < len(block) and block[l1_idx] == block[l2_idx]:
            l1_idx -= 1
            l2_idx += 1
            i += 1
        if l1_idx + 1 == 0 or l2_idx - 1 == len(block) - 1:
            return s + 1
    return None


def possible_splits(block):
    same_id = []
    for i, (l1, l2) in enumerate(zip(block, block[1:])):
        if l1 == l2:
            same_id.append(i)
    return same_id


def part_2(blocks):
    pass


def main():
    lines = input_as_str("input_13.txt")
    blocks = parse_input(lines)
    print("Part 1:", part_1(blocks))
    print("Part 2:", part_2(blocks))


if __name__ == '__main__':
    main()

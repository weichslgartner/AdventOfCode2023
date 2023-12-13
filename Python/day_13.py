from typing import List, Optional, Tuple

from aoc import input_as_str


def transpose(lines: List[str]) -> List[str]:
    return [''.join(s) for s in zip(*lines)]


def parse_input(lines: str) -> List[List[str]]:
    return [block.split() for block in lines.split("\n\n")]


def solve(blocks: List[List[str]], reflect_fun) -> int:
    acc = 0
    for block in blocks:
        if i := reflect_fun(block):
            acc += 100 * i
        else:
            tr_block = transpose(block)
            if i := reflect_fun(tr_block):
                acc += i
    return acc


def reflection_size(block: List[str]) -> Optional[int]:
    same_id, same_id_diff = possible_splits(block)
    if len(same_id) == 0:
        return None
    # if smug_detected_init is set to true, the two initial reflection lines will be set the same and smug is ignored
    return find_split(same_id, block, True)


def reflection_size2(block: List[str]) -> Optional[int]:
    same_id, same_id_diff = possible_splits(block)
    if len(same_id) == 0 and len(same_id_diff) == 0:
        return None
    if len(same_id) > 0:
        s = find_split(same_id, block, False)
        if s is not None:
            return s
    return find_split(same_id_diff, block, True)


def find_split(same_id: List[int], block_init: List[str], smug_detected_init: bool) -> Optional[int]:
    for s in same_id:
        block = block_init.copy()
        smug_detected = smug_detected_init
        l1_idx = s
        l2_idx = s + 1
        if smug_detected:
            block[l1_idx] = block[l2_idx]
        i = 0
        while l1_idx >= 0 and l2_idx < len(block) and block[l1_idx] == block[l2_idx]:
            l1_idx -= 1
            l2_idx += 1
            i += 1
            if l1_idx >= 0 and l2_idx < len(block) and not smug_detected:
                if diff_is_one(block[l1_idx], block[l2_idx]):
                    smug_detected = True
                    block[l1_idx] = block[l2_idx]
        if (l1_idx == -1 or l2_idx == len(block)) and smug_detected:
            return s + 1
    return None


def possible_splits(block: List[str]) -> Tuple[List[int], List[int]]:
    same_id = []
    for i, (l1, l2) in enumerate(zip(block, block[1:])):
        if l1 == l2:
            same_id.append(i)
    same_id_diff = []
    for i, (l1, l2) in enumerate(zip(block, block[1:])):
        if diff_is_one(l1, l2):
            same_id_diff.append(i)
    return same_id, same_id_diff


def diff_is_one(str1: str, str2: str) -> bool:
    return len([i for i, (s1, s2) in enumerate(zip(str1, str2)) if s1 != s2]) == 1


def part_1(blocks: List[List[str]]) -> int:
    return solve(blocks, reflection_size)


def part_2(blocks: List[List[str]]) -> int:
    return solve(blocks, reflection_size2)


def main() -> None:
    lines = input_as_str("input_13.txt")
    blocks = parse_input(lines)
    print("Part 1:", part_1(blocks))
    print("Part 2:", part_2(blocks))  # too low, 24500


if __name__ == '__main__':
    main()

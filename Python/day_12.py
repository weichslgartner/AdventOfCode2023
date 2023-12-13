import functools
from typing import List

from aoc import get_lines


def parse_input(lines):
    spring_list = []
    for line in lines:
        springs, records = line.split(maxsplit=1)
        spring_list.append((list(springs), [int(x) for x in records.split(',')]))
    return spring_list


def gen_record(spring: List[int]):
    stack = []
    record = []
    for s in spring:
        if s == '#':
            stack.append('#')
        elif s == '?':
            break
        else:
            if len(stack) > 0:
                record.append(len(stack))
                stack = []
    if len(stack) > 0:
        record.append(len(stack))
    return record


def is_valid(l1: List[int], l2: List[int]) -> bool:
    return len(l1) == len(l2) and all(i == j for i, j in zip(l1, l2))


def is_valid_part(l1: List[int], l2: List[int]) -> bool:
    if len(l1) == 0:
        return True, True
    for i, j in zip(l1[:-1], l2[:-1]):
        if i != j:
            return False, False
    if len(l1) - 1 >= len(l2):
        return False, False
    return l1[-1] <= l2[len(l1) - 1], l1[-1] == l2[len(l1) - 1]


@functools.cache
def dfs(springs, records, possibilities):
    if '?' not in springs:
        if is_valid(gen_record(springs), records):
            # print("".join(springs))
            possibilities += 1
        return possibilities
    rec_new = gen_record(springs)
    part_valid, sub_complete = is_valid_part(gen_record(springs), records)
    if not part_valid:
         return 0
    idx = springs.index('?')
    spring_tmp = springs
    springs = springs[:idx] + '#' + springs[idx + 1:]
    ret1 = dfs(springs, records, possibilities)
    springs = spring_tmp
    springs = springs[:idx] + '.' + springs[idx + 1:]
    rec_new = gen_record(springs[:idx+1])
    part_valid, sub_complete = is_valid_part(rec_new, records)
    if not part_valid:
        return 0
    if sub_complete:
        rec = list(records)[len(rec_new):]
        rec = tuple(rec)
        ret2 = dfs(springs[idx:], rec, possibilities)
    else:
        ret2 = dfs(springs, records, possibilities)
    return ret1 + ret2


def part_1(spring_list):
    sum = 0
    for springs, record in spring_list:
        sum += dfs(''.join(springs), tuple(record),0)
    return sum


def part_2(spring_list):
    sum = 0
    for springs, record in spring_list:
        folded_springs = springs.copy()
        for _ in range(4):
            folded_springs += ["?"]
            folded_springs += springs
        sum +=  dfs(''.join(folded_springs), tuple(record * 5), 0)
    return sum


def main():
    lines = get_lines("input_12.txt")
    spring_list = parse_input(lines)
    print("Part 1:", part_1(spring_list))
    print("Part 2:", part_2(spring_list))


if __name__ == '__main__':
    main()

from typing import List, Dict, Iterable

from aoc import get_lines, extract_all_ints


def parse_input(lines: List[str]) -> Dict[int, int]:
    scratchcards = {}
    for line in lines:
        tmp, yours = line.split("|", maxsplit=1)
        id_, winning = tmp.split(":", maxsplit=1)
        winning = set(extract_all_ints(winning))
        yours = set(extract_all_ints(yours))
        scratchcards[extract_all_ints(id_)[0]] = len(winning & yours)
    return scratchcards


def part_1(scratchcards: Iterable[int]) -> int:
    return sum(map(lambda x: 2 ** (x - 1),
                   filter(lambda x: x > 0, scratchcards)))


def part_2(scratchcards: Dict[int, int]) -> int:
    stack = list(scratchcards.items())
    points = 0
    while not len(stack) == 0:
        id_, num_winning = stack.pop()
        points += 1
        if num_winning > 0:
            for i in range(1, num_winning + 1):
                stack.append((id_ + i, scratchcards[id_ + i]))
    return points


def main():
    lines = get_lines("input_04.txt")
    scratchcards = parse_input(lines)
    print("Part 1:", part_1(scratchcards.values()))
    print("Part 2:", part_2(scratchcards))


if __name__ == '__main__':
    main()

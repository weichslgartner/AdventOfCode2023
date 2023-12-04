from collections import deque
from queue import Queue

from aoc import get_lines, extract_all_ints


def parse_input(lines):
    scratchcards = {}
    for line in lines:
        tmp, yours = line.split("|", maxsplit=1)
        id_, winning = tmp.split(":", maxsplit=1)
        winning = set(extract_all_ints(winning))
        yours = set(extract_all_ints(yours))
        scratchcards[extract_all_ints(id_)[0]] = len(winning & yours)
    return scratchcards


def part_1(scratchcards):
    return sum(map(lambda x: 2 ** (x - 1),
                   filter(lambda x: x > 0, scratchcards)))


def part_2(scratchcards):
    queue = deque(scratchcards.items())
    points = 0
    while not len(queue) == 0:
        id_, num_winning = queue.popleft()
        points += 1
        if num_winning > 0:
            for i in range(1, num_winning + 1):
                queue.append((id_ + i, scratchcards[id_ + i]))
    return points


def main():
    lines = get_lines("input_04.txt")
    scratchcards = parse_input(lines)
    print("Part 1:", part_1(scratchcards.values()))
    print("Part 2:", part_2(scratchcards))


if __name__ == '__main__':
    main()

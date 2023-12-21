import functools
from collections import defaultdict

from aoc import get_lines, Point, get_neighbours_4

rocks_row = defaultdict(list)
rocks_g = None

def parse_input(lines):
    rocks = set()
    global rocks_row, rocks_g
    start = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                rocks.add(Point(x, y))
                rocks_row[y].append(Point(x, y))
            if c == 'S':
                start = Point(x, y)
    rocks_g = rocks
    return rocks, rocks_row, start, Point(len(lines[0]), len(lines))


def part_1(rocks, start, max_p, steps=64):
    orig = {r for r in rocks}
    orig_max_p = max_p
    queue, next_queue = {start}, set()
    for i in range(steps):
        for el in queue:
            for n in get_neighbours_4(el, max_p):
                if n not in rocks:
                    next_queue.add(n)
        queue, next_queue = next_queue, set()
    return len(queue)


@functools.cache
def is_rock(p, max_p):
    return  Point(p.y % max_p.y,p.x % max_p.x) in rocks_g


def part_2(rocks_row, start, max_p, steps=10):
    queue, next_queue = {start}, set()
    for i in range(steps):
        print(i,count_base(queue,max_p), len(queue))
        for p in queue:
            for n in [Point(p.x - 1, p.y), Point(p.x, p.y - 1), Point(p.x + 1, p.y), Point(p.x, p.y + 1)]:
                if not is_rock(n, max_p):
                    next_queue.add(n)
        queue, next_queue = next_queue, set()
    return len(queue)

def print_grid(max_p):
    for y in range(-max_p.y, max_p.y):
        for x in range(-max_p.x, max_p.x):
            p = Point(x,y)
            if is_rock(p,max_p):
                print("#", end="")
            else:
                print(".", end="")
        print()


def count_base(points, max_p):
    cnt = 0
    for p in points:
        if (p.x // max_p.x) == 0 and  (p.y // max_p.y) == 0:
            cnt+=1
    return cnt


def main():
    lines = get_lines("input_21_test.txt")
    rocks, rocks_row, start, max_p = parse_input(lines)
    assert not is_rock(Point(-2, -1), max_p)

    print("Part 1:", part_1(rocks, start, max_p))
    print("Part 2:", part_2(rocks_row, start, max_p,100))


if __name__ == '__main__':
    main()

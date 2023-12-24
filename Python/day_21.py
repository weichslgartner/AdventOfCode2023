import functools
from collections import defaultdict

from aoc import get_lines, Point
rocks_g = None


def parse_input(lines):
    rocks = set()
    global rocks_g
    start = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                rocks.add(Point(x, y))
            if c == 'S':
                start = Point(x, y)
    rocks_g = rocks
    return rocks, start, Point(len(lines[0]), len(lines))


@functools.cache
def part_1(start, max_p, steps=64):
    queue, next_queue = {start}, set()
    for i in range(steps):
        for p in queue:
            for n in (Point(p.x - 1, p.y), Point(p.x, p.y - 1), Point(p.x + 1, p.y), Point(p.x, p.y + 1)):
                if not is_rock(n, max_p):
                    next_queue.add(n)
        queue, next_queue = next_queue, set()
    return len(queue)


@functools.cache
def is_rock(p, max_p):
    return Point(p.y % max_p.y, p.x % max_p.x) in rocks_g


def part_2(start, max_p, steps=1):
    edge = max_p.x - 1 - start.x
    u0, u1, u2 = (
        part_1(start, max_p, steps=edge + (max_p.x * x))
        for x in range(3)
    )
    a = (u2 - (2 * u1) + u0) // 2
    b = u1 - u0 - a
    c = u0
    x = ((steps - edge) // max_p.x )
    return a * (x ** 2) + b * x + c


def main():
    lines = get_lines("input_21.txt")
    rocks, start, max_p = parse_input(lines)
    print("Part 1:", part_1(start, max_p))
    print("Part 2:", part_2(start, max_p, 26_501_365))


if __name__ == '__main__':
    main()

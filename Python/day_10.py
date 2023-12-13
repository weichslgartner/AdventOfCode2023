from collections import deque
from copy import deepcopy

from aoc import get_lines, Point, get_neighbours_4


def parse_input(lines):
    sym2point = {}
    point2sym = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != '.':
                p = Point(x, y)
                point2sym[p] = c
                sym2point[c] = p
    return sym2point, point2sym


def part_1(sym2point, point2sym):
    cur = [sym2point['S']]
    visited = set(cur)
    steps = 0
    next = []
    point2dist = {}
    while len(cur) > 0:
        for c in cur:
            s = point2sym[c]
            # print(f"{c} {s} {steps}")
            point2dist[c] = steps
            if s == '|':
                add_south(c, next, point2sym, visited)
                add_north(c, next, point2sym, visited)
            elif s == '-':
                add_west(c, next, point2sym, visited)
                add_east(c, next, point2sym, visited)
            elif s == 'F':
                add_south(c, next, point2sym, visited)
                add_east(c, next, point2sym, visited)
            elif s == 'J':
                add_north(c, next, point2sym, visited)
                add_west(c, next, point2sym, visited)
            elif s == '7':
                add_south(c, next, point2sym, visited)
                add_west(c, next, point2sym, visited)
            elif s == 'L':
                add_north(c, next, point2sym, visited)
                add_east(c, next, point2sym, visited)
            elif s == 'S':
                add_south(c, next, point2sym, visited)
                add_north(c, next, point2sym, visited)
                add_west(c, next, point2sym, visited)
                add_east(c, next, point2sym, visited)
        if len(next) > 0:
            steps += 1
        cur, next = next, []
    # print_grid(point2dist, point2sym)

    return steps, visited,point2dist


def print_grid(point2dist, point2sym, inside, outside):
    for y in range(141):
        for x in range(141):
            p = Point(x, y)
            if p in point2dist:
                print(f"{point2dist[p]}", end="")
            elif p in point2sym:
                print(f"{point2sym[p]}", end="")
            else:
                print(f".", end="")
        print()


def print_grid_io(point2sym, inside, outside):
    for y in range(10):
        for x in range(20):
            p = Point(x, y)
            if p in point2sym:
                print(f"{point2sym[p]:3}", end="")
            elif p in inside:
                print(f" I ", end="")
            elif p in outside:
                print(f" O ", end="")
            else:
                print(f".", end="")
        print()


def add_east(c, next, point2sym, visited):
    p = Point(c.x + 1, c.y)
    perhaps_add(next, p, "J-7", point2sym, visited)


def add_west(c, next, point2sym, visited):
    p = Point(c.x - 1, c.y)
    perhaps_add(next, p, "F-L", point2sym, visited)


def add_north(c, next, point2sym, visited):
    p = Point(c.x, c.y - 1)
    perhaps_add(next, p, "F|7", point2sym, visited)


def add_south(c, next, point2sym, visited):
    p = Point(c.x, c.y + 1)
    perhaps_add(next, p, "L|J", point2sym, visited)


def perhaps_add(next, p, poss_syms, point2sym, visited):
    if p in point2sym and point2sym[p] in poss_syms and p not in visited:
        visited.add(p)
        next.append(p)


def part_2(point2sym, visited,point2dist):
    y_min, x_min, y_max, x_max = 145, 145, 0, 0
    print(visited)
    for p in visited:
        print(p)
        y_min, x_min, y_max, x_max = min(p.y, y_min), min(p.x, x_min), max(p.y, y_max), max(p.x, x_max)
    print(y_min, x_min, y_max, x_max)
    p_min = Point(x_min, y_min)
    p_max = Point(x_max, y_max)
    num_inside = 0
    colored = set()
    inside = set()
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            p = Point(x, y)
            if p.x == 14 and p.y == 3:
                print("debug")
            if p in visited or p in colored:
                continue
            outside, col = fill(p, point2sym, p_min, p_max)
            if not outside:
                num_inside += len(col)
                inside |= col
            colored |= col
    print_grid_io(point2dist, inside, colored)
    return num_inside


def fill(point: Point, point2sym, p_min, p_max):
    deq = deque()
    deq.append(point)
    visited = {point}
    outside = False
    while len(deq) > 0:
        p = deq.pop()
        if p.x == p_min.x or p.x == p_max.x or p.y == p_max.y:
            outside = True
        for n in get_neighbours_4(p, Point(145, 145)):
            if n not in point2sym and n not in visited:
                visited.add(n)
                deq.append(n)
    return outside, visited

def in_between(p: Point):
    return ((Point(p.x-1,p.y-1),Point(p.x,p.y-1))
            (Point(p.x,p.y-1),Point(p.x+1,p.y-1))
            (Point(p.x, p.y - 1), Point(p.x, p.y))
            (Point(p.x, p.y ), Point(p.x, p.y+1))
            (Point(p.x - 1, p.y +1), Point(p.x, p.y + 1))
            (Point(p.x, p.y + 1), Point(p.x + 1, p.y + 1))
            (Point(p.x, p.y - 1), Point(p.x, p.y))
            (Point(p.x, p.y), Point(p.x, p.y + 1))
            )



def check_leak(point: Point, point2dist, inside_set):
    deq = deque()
    deq.append(in_between(point))
    visited = {in_between(point)}
    while len(deq) > 0:
        p = deq.pop()
        if p.x == p_min.x or p.x == p_max.x or p.y == p_max.y:
            outside = True
        for n in get_neighbours_4(p, Point(145, 145)):
            if n not in point2sym and n not in visited:
                visited.add(n)
                deq.append(n)
    return False

def main():
    lines = get_lines("input_10_test.txt")
    sym2point, point2sym = parse_input(lines)
    steps, visited,point2dist = part_1(sym2point, point2sym)
    print("Part 1:", steps)
    print("Part 2:", part_2(point2sym, visited,point2dist))


if __name__ == '__main__':
    main()

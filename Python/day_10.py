from collections import deque
from copy import deepcopy
from typing import Tuple

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
    return sym2point, point2sym, Point(len(lines[0]),len(lines))


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

    return steps, visited, point2dist


def print_grid(point2sym, inside, outside):
    for y in range(11):
        for x in range(22):
            p = Point(x, y)
            if p in point2sym:
                print(f"{point2sym[p]}", end="")
            elif p in inside:
                print(f"I", end="")
            elif p in outside:
                print(f"O", end="")
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

def is_point_in_path(p: Point, poly: list[Point]) -> bool:
    num = len(poly)
    j = num - 1
    inside = False
    for i in range(num):
        if (p.x == poly[i].x) and (p.y == poly[i].y):
            # point is a corner
            return True
        if (poly[i].y > p.y) != (poly[j].y > p.y):
            slope = (p.x - poly[i].x) * (poly[j].y - poly[i].y) - (
                poly[j].x - poly[i].x
            ) * (p.y - poly[i].y)
            if slope == 0:
                # point is on boundary
                return True
            if (slope < 0) != (poly[j].y < poly[i].y):
                inside = not inside
        j = i
    return inside

def part_2(point2sym, visited,point2dist,polygon,pmax):
    num_inside = 0
    pol_set = set(polygon)
    for y in range(pmax.y):
        for x in range(pmax.x):
            p = Point(x,y)
            if p not in pol_set and is_point_in_path(p,polygon):
                num_inside += 1
    return num_inside

def part_2_(point2sym, visited,point2dist):
    y_min, x_min, y_max, x_max = 145, 145, 0, 0
    print(visited)
    for p in visited:
       # print(p)
        y_min, x_min, y_max, x_max = min(p.y, y_min), min(p.x, x_min), max(p.y, y_max), max(p.x, x_max)
   # print(y_min, x_min, y_max, x_max)
    p_min = Point(x_min, y_min)
    p_max = Point(x_max, y_max)
    num_inside = 0
    colored = set()
    inside = []
    outside_set = set()
    all_inside = set()
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
                inside.append(col)
                all_inside |= col
            else:
                outside_set |= col
            colored |= col
    tuple_visited = set()
    inside_set = set()
    print(inside)
    for inside_group in inside:
        for i in inside_group:

            outside, tuple_visited, new_inside = check_leak(i, point2dist, i,all_inside,outside_set,tuple_visited)
            if outside:
                num_inside -= len(i)
                all_inside -= new_inside
                outside_set |= new_inside
                #print(inside_group)
            else:
                inside_set.add(i)
    print_grid_io(point2dist, inside, colored)
    print_grid(point2sym, inside_set, colored)
    print(inside_set-set(point2sym))
    return len(inside_set)


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
    return ((Point(p.x-1,p.y-1),Point(p.x,p.y-1)),
            (Point(p.x,p.y-1),Point(p.x+1,p.y-1)),
            (Point(p.x+1, p.y - 1), Point(p.x+1, p.y)),
            (Point(p.x+1, p.y ), Point(p.x+1, p.y+1)),
            (Point(p.x - 1, p.y +1), Point(p.x, p.y + 1)),
            (Point(p.x, p.y + 1), Point(p.x + 1, p.y + 1)),
            (Point(p.x-1, p.y - 1), Point(p.x-1, p.y)),
            (Point(p.x-1, p.y), Point(p.x-1, p.y + 1)),
            )

def get_neighbours_tuples(tup: Tuple[Point,Point]):
    p1,p2 = tup
    #horizontal
    if p1.y!=p2.y:
        assert p1.x==p2.x
        return ((Point(p1.x-1 ,p1.y),Point(p2.x-1,p2.y)),
                (Point(p1.x + 1, p1.y), Point(p2.x + 1, p2.y)),
                (Point(p1.x - 1, p1.y), Point(p2.x, p1.y)),
                (Point(p1.x , p1.y), Point(p2.x+1, p1.y)),
                (Point(p1.x - 1, p2.y), Point(p2.x, p2.y)),
                (Point(p1.x, p2.y), Point(p2.x + 1, p2.y))
                )
    return ((Point(p1.x, p1.y-1),Point(p2.x, p2.y-1)),
            (Point(p1.x, p1.y + 1), Point(p2.x, p2.y + 1)),
            (Point(p1.x, p1.y),Point(p1.x, p1.y-1)),
            (Point(p2.x, p2.y), Point(p2.x, p2.y - 1)),
            (Point(p1.x, p1.y), Point(p1.x, p1.y + 1)),
            (Point(p2.x, p2.y), Point(p2.x, p2.y + 1)),

            )
def check_leak(point: Point, point2dist, inside_set,all_inside,outside_set, visited):
    deq = deque()
    visited = set()
    new_inside = set()
    for ibtw in in_between(point):
        deq.append(ibtw)
        visited.add(ibtw)
    outside = False
    while len(deq) > 0:
        (p1,p2) = deq.pop()
        if p1 in outside_set or p2 in outside_set:
            outside = True
        for n in get_neighbours_tuples((p1,p2)):
            if (leak_between_pipes(n[0], n[1], point2dist) or (n[0] in all_inside or n[1] in all_inside))  and n not in visited:
                visited.add(n)
                deq.append(n)
                if n[0] in all_inside:
                    new_inside.add(n[0])
                if n[1] in all_inside:
                    new_inside.add(n[1])
    return outside, visited, new_inside


def leak_between_pipes(p1, p2, point2dist):
    return p1 in point2dist and p2 in point2dist and abs(point2dist[p1] - point2dist[p2]) == 1

def get_polygon(p,point2dist):
    visited = {p}
    polygon = [p]
    queue = [p]
    while len(queue) > 0:
        p = queue.pop()
        for n in [Point(p.x + 1, p.y), Point(p.x, p.y + 1),Point(p.x - 1, p.y), Point(p.x, p.y - 1)]:
            if n in point2dist and abs(point2dist[n]- point2dist[p])==1 and n not in visited:
                visited.add(n)
                queue.append(n)
                polygon.append(n)
                break
    return polygon

def main():
    lines = get_lines("input_10.txt")
    sym2point, point2sym, pmax = parse_input(lines)
    steps, visited,point2dist = part_1(sym2point, point2sym)
    polygon = get_polygon(sym2point["S"],point2dist)
    print("Part 1:", steps)
    print("Part 2:", part_2(point2sym, visited,point2dist,polygon,pmax))


def print_tuple(t):
    for y in range(4):
        for x in range(4):
            p = Point(x, y)
            if p == t[0] or p == t[1]:
                print("x", end="")
            else:
                print(f".", end="")
        print()
    print()


if __name__ == '__main__':
    main()

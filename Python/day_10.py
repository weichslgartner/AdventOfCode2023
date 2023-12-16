from typing import List

from aoc import get_lines, Point


def parse_input(lines):
    sym2point = {}
    point2sym = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != '.':
                p = Point(x, y)
                point2sym[p] = c
                sym2point[c] = p
    return sym2point, point2sym, Point(len(lines[0]), len(lines))


def part_1(sym2point, point2sym):
    cur = [sym2point['S']]
    visited = set(cur)
    steps = 0
    next_p = []
    point2dist = {}
    while len(cur) > 0:
        for c in cur:
            s = point2sym[c]
            # print(f"{c} {s} {steps}")
            point2dist[c] = steps
            if s == '|':
                add_south(c, next_p, point2sym, visited)
                add_north(c, next_p, point2sym, visited)
            elif s == '-':
                add_west(c, next_p, point2sym, visited)
                add_east(c, next_p, point2sym, visited)
            elif s == 'F':
                add_south(c, next_p, point2sym, visited)
                add_east(c, next_p, point2sym, visited)
            elif s == 'J':
                add_north(c, next_p, point2sym, visited)
                add_west(c, next_p, point2sym, visited)
            elif s == '7':
                add_south(c, next_p, point2sym, visited)
                add_west(c, next_p, point2sym, visited)
            elif s == 'L':
                add_north(c, next_p, point2sym, visited)
                add_east(c, next_p, point2sym, visited)
            elif s == 'S':
                add_south(c, next_p, point2sym, visited)
                add_north(c, next_p, point2sym, visited)
                add_west(c, next_p, point2sym, visited)
                add_east(c, next_p, point2sym, visited)
        if len(next_p) > 0:
            steps += 1
        cur, next_p = next_p, []
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


def add_east(c, next_p, point2sym, visited):
    p = Point(c.x + 1, c.y)
    perhaps_add(next_p, p, "J-7", point2sym, visited)


def add_west(c, next_p, point2sym, visited):
    p = Point(c.x - 1, c.y)
    perhaps_add(next_p, p, "F-L", point2sym, visited)


def add_north(c, next_p, point2sym, visited):
    p = Point(c.x, c.y - 1)
    perhaps_add(next_p, p, "F|7", point2sym, visited)


def add_south(c, next_p, point2sym, visited):
    p = Point(c.x, c.y + 1)
    perhaps_add(next_p, p, "L|J", point2sym, visited)


def perhaps_add(next_p, p, poss_syms, point2sym, visited):
    if p in point2sym and point2sym[p] in poss_syms and p not in visited:
        visited.add(p)
        next_p.append(p)


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


def part_2(polygon: List[Point], pmax: Point) -> int:
    num_inside = 0
    pol_set = set(polygon)
    for y in range(pmax.y):
        for x in range(pmax.x):
            p = Point(x, y)
            if p not in pol_set and is_point_in_path(p, polygon):
                num_inside += 1
    return num_inside


def get_polygon(p, point2dist):
    visited = {p}
    polygon = [p]
    queue = [p]
    while len(queue) > 0:
        p = queue.pop()
        for n in [Point(p.x + 1, p.y), Point(p.x, p.y + 1), Point(p.x - 1, p.y), Point(p.x, p.y - 1)]:
            if n in point2dist and abs(point2dist[n] - point2dist[p]) == 1 and n not in visited:
                visited.add(n)
                queue.append(n)
                polygon.append(n)
                break
    return polygon


def main():
    lines = get_lines("input_10.txt")
    sym2point, point2sym, pmax = parse_input(lines)
    steps, visited, point2dist = part_1(sym2point, point2sym)
    polygon = get_polygon(sym2point["S"], point2dist)
    print("Part 1:", steps)
    print("Part 2:", part_2(polygon, pmax))


if __name__ == '__main__':
    main()

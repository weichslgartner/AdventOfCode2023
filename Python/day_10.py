from aoc import get_lines, Point, get_neighbours_4


def parse_input(lines):
    sym2point = {}
    point2sym = {}
    for y,line in enumerate(lines):
        for x, c in enumerate(line):
            if c != '.':
                p = Point(x,y)
                point2sym[p] = c
                sym2point[c] = p
    return sym2point, point2sym


def part_1(sym2point, point2sym):
    x_max, y_max = max(x for x in point2sym.keys()), max(y for y in point2sym.keys())
    p_max = Point(x_max,y_max)
    cur = [sym2point['S']]
    visited = set(cur)
    steps = 0
    next = []
    while len(cur) > 0:
        for el in cur:
            c = cur.pop()
            s = point2sym[c]
            if c == '|':
                add_south(c, next, point2sym, visited)
                add_north(c, next, point2sym, visited)
            if c == '-':
                add_west(c, next, point2sym, visited)
                add_east(c, next, point2sym, visited)
            if c == 'F':
                add_south(c, next, point2sym, visited)
                add_east(c, next, point2sym, visited)
            if c == 'J':
                add_north(c, next, point2sym, visited)
                add_west(c, next, point2sym, visited)
            steps += 1
        cur, next = next, []
    return steps


def add_east(c, next, point2sym, visited):
    p = Point(c.x + 1, c.y)
    perhaps_add(next, p, "J-7", point2sym, visited)


def add_west(c, next, point2sym, visited):
    p = Point(c.x - 1, c.y)
    perhaps_add(next, p, "F-L", point2sym, visited)


def add_north(c, next, point2sym, visited):
    p = Point(c.x, c.y + 1)
    perhaps_add(next, p, "L|J", point2sym, visited)


def add_south(c, next, point2sym, visited):
    p = Point(c.x, c.y - 1)
    perhaps_add(next, p, "F|7", point2sym, visited)


def perhaps_add(next, p, poss_syms,point2sym, visited):
    if point2sym[p] in poss_syms and p not in visited:
        visited.add(p)
        next.add(p)


def get_next(c:Point, p_max,sym2point, point2sym):
    for n in get_neighbours_4(c, p_max):
        s = point2sym[c]
        next.append(n)


def part_2(lines):
    pass


def main():
    lines = get_lines("input_10.txt")
    sym2point, point2sym = parse_input(lines)
    print("Part 1:", part_1(sym2point, point2sym))
    print("Part 2:", part_2(sym2point, point2sym))


if __name__ == '__main__':
    main()

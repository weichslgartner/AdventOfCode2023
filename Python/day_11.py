from itertools import combinations

from aoc import get_lines, Point, get_neighbours_4, manhattan_distance


def parse_input(lines):
    point2galaxy = {}
    id = 1
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != '.':
                p = Point(x, y)
                point2galaxy[p] = id
                id += 1
    return point2galaxy, Point(len(lines[0]), len(lines))


def part_1(point2galaxy, pmax):
    y_expand = [y for y in range(pmax.y) if all(Point(x, y) not in point2galaxy for x in range(pmax.x))]
    x_expand = [x for x in range(pmax.x) if all(Point(x, y) not in point2galaxy for y in range(pmax.y))]
    for i,y_plus in enumerate(y_expand):
        for p in list(point2galaxy.keys()):
            if p.y > y_plus+i:
                point2galaxy[Point(p.x, p.y+1)] = point2galaxy.pop(p)
    for i,x_plus in enumerate(x_expand):
        for p in list(point2galaxy.keys()):
            if p.x > x_plus+i:
                point2galaxy[Point(p.x+1, p.y)] = point2galaxy.pop(p)
    #print_grid(point2galaxy, Point(pmax.x+len(x_expand),pmax.y+len(y_expand)))
    #print(x_expand, y_expand)
    sum = 0
    pairs = {}
    for i,j in combinations(point2galaxy.keys(),2):
        pairs[(point2galaxy[i],point2galaxy[j])] = manhattan_distance(i,j)
        sum += manhattan_distance(i,j)
    #print(pairs)
    #print(len(pairs))
    return sum

def print_grid(point2dist, pmax):
    for y in range(pmax.y):
        for x in range(pmax.x):
            p = Point(x, y)
            if p in point2dist:
                print(f"{point2dist[p]}", end="")
            else:
                print(f".", end="")
        print()

def part_2(point2galaxy):
    pass


def main():
    lines = get_lines("input_11.txt")
    point2galaxy, pmax = parse_input(lines)
    print("Part 1:", part_1(point2galaxy, pmax))
    print("Part 2:", part_2(point2galaxy))


if __name__ == '__main__':
    main()

from typing import Dict

from aoc import get_lines, Point, Direction, point_to_dir, is_in_grid, dir_to_point


def parse_input(lines):
    p2sym = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != '.':
                p2sym[Point(x, y)] = c
    return p2sym, Point(len(lines[0]), len(lines))


def get_next(sym: str, sym_p: Point, direc: Direction) -> tuple[list[Point], list[Direction]]:
    diff_p = dir_to_point(direc)
    # diff_p = Point(x=sym_p.x-p.x,y=sym_p.y-p.y)
    from_x = direc == Direction.EAST or direc == Direction.WEST
    from_y = direc == Direction.SOUTH or direc == Direction.NORTH
    match sym:
        case "\\":
            if from_x:
                return [Point(sym_p.x, sym_p.y + diff_p.x)], [point_to_dir(Point(0, diff_p.x))]
            return [Point(sym_p.x + diff_p.y, sym_p.y)], [point_to_dir(Point(diff_p.y, 0))]
        case '/':
            if from_x:
                return [Point(sym_p.x, sym_p.y - diff_p.x)], [point_to_dir(Point(0, -diff_p.x))]
            return [Point(sym_p.x - diff_p.y, sym_p.y)], [point_to_dir(Point(-diff_p.y, 0))]
        case '|':
            if from_x:
                return [Point(sym_p.x, sym_p.y - 1), Point(sym_p.x, sym_p.y + 1)], [Direction.NORTH, Direction.SOUTH]
            return [Point(sym_p.x, sym_p.y + diff_p.y)], [point_to_dir(diff_p)]
        case '-':
            if from_y:
                return [Point(sym_p.x + 1, sym_p.y), Point(sym_p.x - 1, sym_p.y)], [Direction.EAST, Direction.WEST]
            return [Point(sym_p.x + diff_p.x, sym_p.y)], [point_to_dir(diff_p)]


def part_1(p2sym: Dict[Point, str], p_max: Point) -> int:
    return solve(p2sym, p_max, Point(0, 0), Direction.EAST)


def solve(p2sym: Dict[Point, str], p_max: Point, start_p: Point, start_dir: Direction) -> int:
    cur = [(start_p, start_dir)]
    visited_p = set()
    visited = set()
    while len(cur) > 0:
        p, d = cur.pop()
        visited.add((p, d))
        if is_in_grid(p, p_max):
            visited_p.add(p)
            if p in p2sym:
                ps, ds = get_next(p2sym[p], p, d)
                for p_, d_ in zip(ps, ds):
                    if (p_, d_) not in visited:
                        cur.append((p_, d_))
            else:
                diff_p = dir_to_point(d)
                to_add = (Point(p.x + diff_p.x, p.y + diff_p.y), d)
                if to_add not in visited:
                    cur.append(to_add)

    return len(visited_p)


def part_2(p2sym: Dict[Point, str], p_max: Point) -> int:
    max_act = 0
    for y in range(p_max.y):
        max_act = max(max_act, solve(p2sym, p_max, Point(0, y), Direction.EAST))
        max_act = max(max_act, solve(p2sym, p_max, Point(p_max.x - 1, y), Direction.WEST))
    for x in range(p_max.x):
        max_act = max(max_act, solve(p2sym, p_max, Point(x, 0), Direction.SOUTH))
        max_act = max(max_act, solve(p2sym, p_max, Point(x, p_max.y - 1), Direction.NORTH))
    return max_act


def main():
    lines = get_lines("input_16.txt")
    p2sym, p_max = parse_input(lines)
    print("Part 1:", part_1(p2sym, p_max))
    print("Part 2:", part_2(p2sym, p_max))  # 8357 too low


if __name__ == '__main__':
    main()

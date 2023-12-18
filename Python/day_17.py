import heapq
import sys
from collections import namedtuple, deque, defaultdict

from aoc import get_lines, Point, Direction, get_neighbours_4, point_to_dir, manhattan_distance, dir_to_point


class Element(namedtuple('Element', 'p dirs heat_loss')):
    def __repr__(self):
        return f'{self.p} {self.dirs} {self.heat_loss}'


def parse_input(lines):
    return [[int(x) for x in line] for line in lines]


def part_1(grid, start=Point(0, 0)):
    # print(grid)
    max_p = Point(len(grid[0]), len(grid))
    target = Point(max_p.x - 1, max_p.y - 1)
    min_dist = sys.maxsize
    res = ""
    queue = [(manhattan_distance(start, target), Element(start, "", 0))]
    heapq.heapify(queue)
    visited = defaultdict(lambda: sys.maxsize)
    while len(queue) > 0:
        _, el = heapq.heappop(queue)
        # in_queue.remove(el.p)
        # print(el)
        if target == el.p and el.heat_loss <= min_dist:
            min_dist = min(min_dist, el.heat_loss)
            res = el.dirs
            # print("new",el.dirs,min_dist)
            continue
        if el.heat_loss > min_dist:
            continue
        ns = list(get_neighbours_4(el.p, max_p))
        # print(ns)
        for n in ns:
            diff_p = Point(n.x - el.p.x, n.y - el.p.y)
            d = point_to_dir(diff_p)
            if len(el.dirs) > 2:
                # assert len(el.dirs) == 3
                if all(d == c for c in el.dirs[-3:]):
                    continue
                new_dirs = el.dirs[-2:] + str(d)
            else:
                new_dirs = el.dirs + str(d)
            if new_dirs[-2:] == "><" or new_dirs[-2:] == "v^":
                continue
            if visited[(n, new_dirs)] > el.heat_loss + grid[n.y][n.x]:  # and n not  in in_queue :
                visited[(n, new_dirs)] = el.heat_loss + grid[n.y][n.x]
                heapq.heappush(queue, (manhattan_distance(n, target), Element(n, new_dirs, visited[(n, new_dirs)])))
    # for y, line in enumerate(grid):
    #     for x, c in enumerate(line):
    #         p = Point(x, y)
    #         v_value = min(visited[(p, c)] for c in "<>^v")
    #         if v_value != sys.maxsize:
    #             print(f"|{v_value:3}|", end="")
    #
    #         else:
    #             print(f"|###|", end="")
    #             # print(f"{grid[x][y]}", end="")
    #    # print()
    return min_dist, res


def part_2(lines):
    pass


def print_grid(grid, s=">v>>^>>>v>>v>>vv>v>vvv<v>vvv", start=Point(1, 0)):
    l = [start]
    sum = grid[l[-1].y][l[-1].x]
    for c in s[1:]:
        diff = dir_to_point(c)
        l.append(Point(l[-1].x + diff.x, l[-1].y + diff.y))
        sum += grid[l[-1].y][l[-1].x]
    print("sum", sum)
    dict = {p: c for p, c in zip(l, s)}
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            p = Point(x, y)
            if p in dict:
                print(f"{dict[p]}", end="")
            else:
                print(f".", end="")
                # print(f"{grid[x][y]}", end="")
        print()


def main():
    lines = get_lines("input_17.txt")  # 861 too low, 907 too high
    grid = parse_input(lines)
    part1, res = part_1(grid)
    # print_grid(grid,s=res,start=Point(0,1))
    print("Part 1:", part1)
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()

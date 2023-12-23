from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple

from aoc import get_lines, Point3


# @dataclass
# class Point3():
#     x: int
#     y: int
#     z: int
#     def __repr__(self):
#         return f'{self.x},{self.y},{self.z}'


def parse_input(lines):
    shapes = []
    for line in lines:
        p1_str, p2_str = line.split("~", 1)
        shapes.append((Point3(*map(int, p1_str.split(",", 2))), Point3(*map(int, p2_str.split(",", 2)))))
    print(shapes)
    return sorted(shapes, key=lambda x: min(x[0].z, x[1].z))


def part_1(shapes: List[Tuple[Point3, Point3]]) -> int:
    max_x, max_y = max(shapes, key=lambda s: s[1].x)[1].x, max(shapes, key=lambda s: s[1].y)[1].y
    top = [[(0, -1) for x in range(0, max_x + 1)] for y in range(0, max_y + 1)]
    rests_list = defaultdict(set)
    for i, shape in enumerate(shapes):
        block_rests(rests_list, shape, top, i)
        for y in range(0, max_y + 1):
            for x in range(0, max_x + 1):
                print(top[y][x], end="")
            print()
        print("===")
    del rests_list[-1]
    print(rests_list)

    supported_by = defaultdict(set)

    for k, vals in rests_list.items():
        for v in vals:
            supported_by[v].add(k)
    print(supported_by)
    allshapes = {i for i in range(len(shapes))}
    critical_shapes = set()
    for v in supported_by.values():
        if len(v) == 1:
            critical_shapes.add(v.pop())
    part_a =  len(allshapes -critical_shapes)
    overall = part_b(rests_list, supported_by, critical_shapes)
    return  part_a, overall


def part_b(rests_list, supported_by, critical_shapes):
    overall = 0
    print(critical_shapes)
    for crit in critical_shapes:
        queue = {crit}
        next_q = set()
        while len(queue) > 0:
            to_remove = set()
            for q in queue:
                to_remove |= rests_list[q]
            for r in to_remove:
                if len(supported_by[r] - queue) == 0:
                    overall +=1
                    next_q.add(r)
            queue,next_q = next_q,set()

    return overall


def block_rests(rest_set, shape, top, id_) -> bool:
    max_p = 0
    laying_on = defaultdict(set)
    if shape[0].y != shape[1].y:
        for i in range(shape[0].y, shape[1].y + 1):
            if top[i][shape[0].x][0] > max_p:
                max_p = top[i][shape[0].x][0]
                laying_on.clear()
                laying_on[top[i][shape[0].x][1]].add(id_)
            # laying_on[top[i][shape[0].x][1]].add(id_)
            elif top[i][shape[0].x][0] == max_p:
                laying_on[top[i][shape[0].x][1]].add(id_)
        for i in range(shape[0].y, shape[1].y + 1):
            top[i][shape[0].x] = (max_p + 1, id_)
    elif shape[0].x != shape[1].x:
        for i in range(shape[0].x, shape[1].x + 1):
            if top[shape[0].y][i][0] > max_p:
                max_p = top[shape[0].y][i][0]
                laying_on.clear()
                laying_on[top[shape[0].y][i][1]].add(id_)
            elif top[shape[0].y][i][0] == max_p:
                laying_on[top[shape[0].y][i][1]].add(id_)
        for i in range(shape[0].x, shape[1].x + 1):
            top[shape[0].y][i] = (max_p + 1, id_)
    else:
        laying_on[top[shape[0].y][shape[0].x][1]].add(id_)
        top[shape[0].y][shape[0].x] = (top[shape[0].y][shape[0].x][0] + shape[1].z - shape[0].z + 1, id_)
    for k, v in laying_on.items():
        rest_set[k] |= v


def part_2(lines):
    pass


def main():
    lines = get_lines("input_22.txt")
    shapes = parse_input(lines)
    p1,p2 = part_1(shapes)
    print("Part 1:", p1)
    print("Part 2:", p2) #82042 too low


if __name__ == '__main__':
    main()

from collections import defaultdict

from aoc import get_lines, Point3


def parse_input(lines):
    shapes = []
    for line in lines:
        p1_str, p2_str = line.split("~", 1)
        shapes.append((Point3(*map(int, p1_str.split(",", 2))), Point3(*map(int, p2_str.split(",", 2)))))
    return sorted(shapes, key=lambda x: min(x[0].z, x[1].z))


def gen_shapes(shapes):
    max_x, max_y = max(shapes, key=lambda s: s[1].x)[1].x, max(shapes, key=lambda s: s[1].y)[1].y
    top = [[(0, -1) for x in range(0, max_x + 1)] for y in range(0, max_y + 1)]
    rests_list = defaultdict(set)
    for i, shape in enumerate(shapes):
        block_rests(rests_list, shape, top, i)
    supported_by = defaultdict(set)
    for k, vals in rests_list.items():
        for v in vals:
            supported_by[v].add(k)
    allshapes = {i for i in range(len(shapes))}
    critical_shapes = set()
    for v in supported_by.values():
        if len(v) == 1:
            critical_shapes.add(next(iter(v)))
    return allshapes, critical_shapes, supported_by


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


def part_1(allshapes, critical_shapes) -> int:
    return len(allshapes - critical_shapes)


def part_2(n_shapes, supported_by):
    overall = 0
    for i in range(n_shapes):
        removed_bricks = set([i])
        for j in range(i + 1, n_shapes):
            if len(supported_by[j] - removed_bricks) == 0:
                removed_bricks.add(j)
                overall += 1
    return overall


def main():
    lines = get_lines("input_22.txt")
    shapes = parse_input(lines)
    allshapes, critical_shapes, supported_by = gen_shapes(shapes)
    print("Part 1:", part_1(allshapes, critical_shapes))
    print("Part 2:", part_2(len(shapes), supported_by))


if __name__ == '__main__':
    main()

from itertools import combinations

import numpy as np
from z3 import Solver, BitVec, BitVecs, BitVecVal, Real, RealVal, Reals, sat

from aoc import get_lines


def parse_input(lines):
    point_vec = []
    for line in lines:
        point, vec = line.split("@", 1)
        point_vec.append((np.array([int(i.strip()) for i in point.split(",")]),
                          np.array([int(i.strip()) for i in vec.split(",")])))
    return point_vec


def find_intersection(point1, vec1, point2, vec2):
    point1, vec1, point2, vec2 = point1.T, vec1.T, point2.T, vec2.T
    x, err, rank = np.linalg.lstsq(np.array([vec1, -vec2]).T, point2 - point1, rcond=None)[:3]
    if rank == 2:
        return vec1 * x[0] + point1
    return None


def part_1(point_vecs, min_p=200000000000000, max_p=400000000000000):
    inside_cross = 0
    for a, b in combinations(point_vecs, r=2):
        point1, vector1 = a
        point2, vector2 = b
        ip = find_intersection(point1[:2], vector1[:2], point2[:2], vector2[:2])
        if ip is not None and min_p <= ip[0] < max_p and min_p <= ip[1] <= max_p:
            if np.all(np.sign(ip - (point1[:2])) == np.sign((vector1[:2]))) and np.all(
                    np.sign(ip - (point2[:2])) == np.sign((vector2[:2]))):
                inside_cross += 1
    return inside_cross


def part_2(point_vecs):
    solver = Solver()
    x, y, z = Reals('x y z')
    vx, vy, vz = Reals('vx vy vz')
    for i, (point1, vector1) in enumerate(point_vecs):
        t = Real(f't{i}')
        solver.add(t >= 0)
        solver.add(x + t * vx == point1[0] + t * vector1[0])
        solver.add(y + t * vy == point1[1] + t * vector1[1])
        solver.add(z + t * vz == point1[2] + t * vector1[2])
    assert solver.check() == sat
    return solver.model().evaluate(x + y + z).as_long()


def main():
    lines = get_lines("input_24.txt")
    point_vec = parse_input(lines)
    print("Part 1:", part_1(point_vec))
    print("Part 2:", part_2(point_vec))


if __name__ == '__main__':
    main()

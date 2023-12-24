from itertools import combinations

from aoc import get_lines
import numpy as np


def parse_input(lines):
    point_vec = []
    for line in lines:
        point, vec = line.split("@", 1)
        point_vec.append(([int(i.strip()) for i in point.split(",")], [int(i.strip()) for i in vec.split(",")]))
    return point_vec


def find_intersection(c1, v1, c2, v2):
    c1, v1, c2, v2 = c1.T, v1.T, c2.T, v2.T
    x, err, rank = np.linalg.lstsq(np.array([v1, -v2]).T, c2 - c1,rcond=None)[:3]
    if rank == 2:
        # intersection exists
        return v1 * x[0] + c1
    return None


def part_1(point_vecs, min_p=200000000000000, max_p=400000000000000):
    #print(point_vecs)
    inside_cross = 0
    for a, b in combinations(point_vecs, r=2):
        point1, vector1 = a
        point2, vector2 = b
        ip = find_intersection(np.array(point1[:2]), np.array(vector1[:2]), np.array(point2[:2]), np.array(vector2[:2]))
        #print(a, b, ip)
        if ip is not None and min_p <= ip[0] < max_p and min_p <= ip[1] <= max_p:
            if all(np.sign(ip - np.array(point1[:2])) == np.sign(np.array(vector1[:2]))) and all(
                    np.sign(ip - np.array(point2[:2])) == np.sign(np.array(vector2[:2]))):
                inside_cross += 1
    return inside_cross


def part_2(lines):
    pass


def main():
    lines = get_lines("input_24.txt")
    point_vec = parse_input(lines)
    print("Part 1:", part_1(point_vec))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()

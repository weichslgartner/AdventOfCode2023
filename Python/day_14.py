from aoc import get_lines
from operator import gt, lt

N_ROWS = None
N_COLS = None
CUBES_TR = None
CUBES = None


def parse_input(lines):
    global N_ROWS, N_COLS, CUBES_TR, CUBES
    rounds = [[] for _ in range(len(lines[0]))]
    cube = [[] for _ in range(len(lines[0]))]
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                cube[x].append(y)
            elif c == "O":
                rounds[x].append(y)
    N_ROWS = len(lines)
    N_COLS = len(lines[0])
    CUBES = tuple(cube)
    CUBES_TR = tuple(transpose(cube, N_COLS))
    return rounds, cube, len(lines), len(lines[0])


def tilt_north(rounds, cubes=CUBES):
    return tilt(rounds, cubes, cur_round_init=-1, cur_cube_init=-1, rev=False)


def tilt_south(rounds, cubes=CUBES):
    return tilt(rounds, cubes, cur_round_init=N_ROWS, cur_cube_init=N_ROWS, rev=True)


def tilt_west(rounds, cubes=CUBES_TR):
    rounds_tr = tilt(transpose(rounds, N_COLS), cubes, cur_round_init=-1, cur_cube_init=-1,
                     rev=False)
    return transpose(rounds_tr, N_ROWS)


def tilt_east(rounds, cubes=CUBES_TR):
    rounds_tr = tilt(transpose(rounds, N_COLS), cubes, cur_round_init=N_COLS, cur_cube_init=N_COLS,
                     rev=True)
    return transpose(rounds_tr, N_ROWS)


def tilt(rounds, cubes, cur_round_init=-1, cur_cube_init=-1, rev=False):
    # print(rounds,cubes)
    cmp = lt if rev else gt
    min_max = min if rev else max

    for x, (r, c) in enumerate(zip(rounds, cubes)):
        cur_round = cur_round_init
        cur_cube = cur_cube_init
        offset = -1 if rev else 1
        cidx = (len(c) - 1) if rev else 0
        rang = reversed(range(len(r))) if rev else range(len(r))
        for i in rang:
            while cidx < len(c) and cidx >= 0 and cmp(r[i], c[cidx]):
                cur_cube = c[cidx]
                cidx += offset
            r[i] = min_max(cur_cube + offset, cur_round + offset)
            cur_round = r[i]
    # print(rounds, cubes)
    return rounds


def tilt_reverse(rounds, cubes, cmp=gt, min_max=max, cur_round_init=-1, cur_cube_init=-1):
    # print(rounds,cubes)
    for x, (r, c) in enumerate(zip(rounds, cubes)):
        cur_round = cur_round_init
        cur_cube = cur_cube_init
        cidx = 0
        for i in reversed(range(len(r))):
            while cidx < len(c) and cmp(r[i], c[cidx]):
                cur_cube = c[cidx]
                cidx += 1
            r[i] = min_max(cur_cube - 1, cur_round - 1)
            cur_round = r[i]
    # print(rounds, cubes)
    return rounds


def calc_score(length, rounds):
    return sum(length - r for roun in rounds for r in roun)


def transpose(src, target):
    dst = [[] for _ in range(target)]
    for y, line in enumerate(src):
        for c in line:
            dst[c].append(y)
    return dst


def part_1(rounds, cubes, length):
    return calc_score(length, tilt_north(rounds, cubes))


def part_2(rounds, cube, n_rows, n_cols, n_cycles=1_000_000_000):
    visited = {}
    scores = {}
    for i in range(n_cycles):
        rounds = do_cycle(rounds)
        round_tup = tuple(tuple(r) for r in rounds)
        if round_tup in visited:
            to_go = n_cycles - i - 1
            period = i - visited[round_tup]
            cycles = to_go // period
            return scores[visited[round_tup] + (n_cycles - (i + cycles * period)) - 1]
        visited[round_tup] = i
        scores[i] = calc_score(n_rows, rounds)
    return calc_score(n_rows, rounds)


def do_cycle(rounds):
    rounds = tilt_north(rounds, CUBES)
    rounds = tilt_west(rounds, CUBES_TR)
    rounds = tilt_south(rounds, CUBES)
    rounds = tilt_east(rounds, CUBES_TR)
    return rounds


def main():
    lines = get_lines("input_14.txt")
    round, cube, n_rows, n_cols = parse_input(lines)
    print("Part 1:", part_1(round, cube, n_rows))
    print("Part 2:", part_2(round, cube, n_rows, n_cols))


if __name__ == '__main__':
    main()

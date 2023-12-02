from aoc import get_lines
from math import prod


def parse_input(lines):
    games = {}
    for line in lines:
        game_id, draws = line.split(":", maxsplit=1)
        game_id = int(game_id.split(" ", maxsplit=1)[-1])
        games[game_id] = []
        for draw in draws.split(";"):
            rev = {}
            for rev_set in draw.split(","):
                _, num, color = rev_set.split(" ", maxsplit=2)
                rev[color] = int(num)
            games[game_id].append(rev)
    return games


def part_1(games):
    constraints = {'red': 12, 'green': 13, 'blue': 14}
    return sum(game_id for game_id, _ in filter(lambda x: is_valid(constraints, x[1]), games.items()))


def is_valid(constraints, game):
    for draw in game:
        for color, num in draw.items():
            if num > constraints[color]:
                return False
    return True


def part_2(games):
    return sum(calc_power(game) for _, game in games.items())


def calc_power(game):
    min_conf = {}
    for draw in game:
        for color, num in draw.items():
            if color not in min_conf or min_conf[color] < num:
                min_conf[color] = num
    return prod(min_conf.values())


def main():
    lines = get_lines("input_02.txt")
    games = parse_input(lines)
    print("Part 1:", part_1(games))
    print("Part 2:", part_2(games))


if __name__ == '__main__':
    main()

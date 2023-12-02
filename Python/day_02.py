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
    allowed_sum = 0
    for game_id, game in games.items():
        if is_valid(constraints, game):
            allowed_sum += game_id
    return allowed_sum


def is_valid(constraints, game):
    for draw in game:
        for color, num in draw.items():
            if num > constraints[color]:
                return False
    return True


def part_2(games):
    min_sum = 0
    for _, game in games.items():
        min_conf = {}
        for draw in game:
            for color, num in draw.items():
                if color not in min_conf or min_conf[color] < num:
                    min_conf[color] = num
        min_sum += prod(min_conf.values())
    return min_sum


def main():
    lines = get_lines("input_02.txt")
    games = parse_input(lines)
    print("Part 1:", part_1(games))
    print("Part 2:", part_2(games))


if __name__ == '__main__':
    main()

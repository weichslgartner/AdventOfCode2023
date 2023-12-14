from aoc import get_lines


def parse_input(lines):
    round = [[] for _ in range(len(lines[0]))]
    cube = [[] for _ in range(len(lines[0]))]
    for y,line in enumerate(lines):
        for x,c in enumerate(line):
            if c=='#':
                cube[x].append(y)
            elif c=="O":
                round[x].append(y)

    return round,cube,len(lines)


def part_1( rounds,cubes,length):
    #print(rounds,cubes)
    for x,(r,c) in enumerate(zip(rounds,cubes)):
        cur_round = -1
        cur_cube = -1
        cidx = 0
        for i in range(len(r)):
            while  cidx < len(c) and r[i] > c[cidx]:
                cur_cube = c[cidx]
                cidx += 1
            r[i] = max(cur_cube+1,cur_round+1)
            cur_round = r[i]
    #print(rounds, cubes)

    return sum( length-r for roun in rounds for r in roun )


def part_2(round,cube):
    pass


def main():
    lines = get_lines("input_14.txt")
    round, cube, length = parse_input(lines)
    print("Part 1:", part_1( round,cube,length))
    print("Part 2:", part_2( round,cube))


if __name__ == '__main__':
    main()

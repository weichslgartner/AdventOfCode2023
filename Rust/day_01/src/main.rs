fn part1(input: &str) -> u32 {
    solve(input, false)
}

fn part2(input: &str) -> u32 {
    solve(input, true)
}

fn solve(input: &str, part2: bool) -> u32 {
    input
        .lines()
        .map(|line| {
            line.chars()
                .enumerate()
                .filter_map(|(i, c)| {
                    c.to_digit(10)
                        .or(if part2 { words_to_num(i, &line) } else { None })
                })
                .collect::<Vec<u32>>()
        })
        .map(|digits| digits.get(0).unwrap() * 10 + digits.last().unwrap())
        .sum()
}

fn words_to_num(i: usize, line: &str) -> Option<u32> {
    let lut = vec![
        ("one", 1),
        ("two", 2),
        ("three", 3),
        ("four", 4),
        ("five", 5),
        ("six", 6),
        ("seven", 7),
        ("eight", 8),
        ("nine", 9),
    ];

    for (old, new) in lut.iter() {
        if let Some(substr) = line.get(i..i + old.len()) {
            if substr == *old {
                return Some(*new);
            }
        }
    }

    None
}

fn main() {
    let input = include_str!("../../../inputs/input_01.txt");
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}

use std::iter::zip;

#[derive(Debug, Copy, Clone)]
struct Race {
    time: usize,
    distance: usize,
}

fn parse_input(input: &str) -> (Vec<Race>, Vec<Race>) {
    let mut times: Vec<&str> = vec![];
    let mut distances: Vec<&str> = vec![];

    for (n, line) in input.lines().enumerate() {
        let (_, nums) = line.split_once(':').unwrap();
        let nums = nums.split_whitespace().collect();
        if n == 0 {
            times = nums;
        } else {
            distances = nums;
        };
    }

    let mut result = vec![];
    let mut time_2: String = "".to_string();
    let mut distance_2: String = "".to_string();

    for (t, d) in zip(times, distances) {
        result.push(Race {
            time: t.parse().unwrap(),
            distance: d.parse().unwrap(),
        });
        time_2 += t;
        distance_2 += d;
    }
    (
        result,
        vec![Race {
            time: time_2.parse().unwrap(),
            distance: distance_2.parse().unwrap(),
        }],
    )
}

fn part_1(races: &Vec<Race>) -> usize {
    solve(races)
}

fn part_2(races: &Vec<Race>) -> usize {
    solve(races)
}

fn solve(races: &Vec<Race>) -> usize {
    let mut points = 1;
    for race in races {
        let a = -1.0;
        let b = race.time as f64;
        let c = -1.0 * race.distance as f64;
        let discriminant = b.powi(2) - 4.0 * a * c;
        if discriminant >= 0.0 {
            let solution1 = (-b + discriminant.sqrt()) / (2.0 * a);
            let solution2 = (-b - discriminant.sqrt()) / (2.0 * a);
            points *= ((solution2 - 1.0).ceil() - (solution1 + 1.0).floor()) as usize + 1;
        }
    }
    points
}

fn main() {
    let input = include_str!("../../../inputs/input_06.txt");
    let (races,race2) = parse_input(input);
    println!("Part 1: {}", part_1(&races));
    println!("Part 2: {}", part_2(&race2));
}

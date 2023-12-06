use std::iter::zip;

#[derive(Debug, Copy, Clone)]
struct Race {
    time: usize,
    distance: usize,
}

impl From<(String, String)> for Race {
    fn from(tup: (String, String)) -> Self {
        Race {
            time: tup.0.parse().unwrap(),
            distance: tup.1.parse().unwrap(),
        }
    }
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

    let result: Vec<Race> = zip(times, distances)
        .map(|(t, d)| Race {
            time: t.parse().unwrap(),
            distance: d.parse().unwrap(),
        })
        .collect();

    (
        vec![Race::from(result.iter().fold(
            ("".to_string(), "".to_string()),
            |(mut time, mut distance), x| {
                time += &x.time.to_string();
                distance += &x.distance.to_string();
                (time, distance)
            },
        ))],
        result,
    )
}

fn part_1(races: &[Race]) -> usize {
    solve(races)
}

fn part_2(races: &[Race]) -> usize {
    solve(races)
}

fn solve(races: &[Race]) -> usize {
    races
        .iter()
        .map(|race| {
            let a = -1.0;
            let b = race.time as f64;
            let c = -1.0 * race.distance as f64;
            let discriminant = b.powi(2) - 4.0 * a * c;
            let solution1 = (-b + discriminant.sqrt()) / (2.0 * a);
            let solution2 = (-b - discriminant.sqrt()) / (2.0 * a);
            ((solution2 - 1.0).ceil() - (solution1 + 1.0).floor()) as usize + 1
        })
        .product()
}

fn main() {
    let input = include_str!("../../../inputs/input_06.txt");
    let (race2, races) = parse_input(input);
    println!("Part 1: {}", part_1(&races));
    println!("Part 2: {}", part_2(&race2));
}

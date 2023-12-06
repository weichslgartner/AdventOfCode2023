use itertools::Itertools;
use std::iter::zip;
#[derive(Debug, Copy, Clone)]
struct Race {
    time: f64,
    distance: f64,
}

impl From<(String, String)> for Race {
    fn from(tup: (String, String)) -> Self {
        Race {
            time: tup.0.parse().unwrap(),
            distance: tup.1.parse().unwrap(),
        }
    }
}

fn parse_input(input: &str) -> Option<(Vec<Race>, Vec<Race>)> {
    let (times, distances): (Vec<&str>, Vec<&str>) = input
        .lines()
        .map(|line| {
            let (_, nums) = line.split_once(':').unwrap();
            nums.split_whitespace().collect::<Vec<&str>>()
        })
        .collect_tuple()?;
    Some((
        zip(&times, &distances)
            .map(|(t, d)| Race {
                time: t.parse().unwrap(),
                distance: d.parse().unwrap(),
            })
            .collect(),
        vec![Race::from(zip(times, distances).fold(
            ("".to_string(), "".to_string()),
            |(mut time, mut distance), (t, d)| {
                time += t;
                distance += d;
                (time, distance)
            },
        ))],
    ))
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
            let b = race.time;
            let c = -1.0 * race.distance;
            let discriminant = b.powi(2) - 4.0 * a * c;
            let solution1 = (-b + discriminant.sqrt()) / (2.0 * a);
            let solution2 = (-b - discriminant.sqrt()) / (2.0 * a);
            ((solution2 - 1.0).ceil() - (solution1 + 1.0).floor()) as usize + 1
        })
        .product()
}

fn main() {
    let input = include_str!("../../../inputs/input_06.txt");
    let (races, race2) = parse_input(input).unwrap();
    println!("Part 1: {}", part_1(&races));
    println!("Part 2: {}", part_2(&race2));
}

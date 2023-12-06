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

#[allow(dead_code)]
fn brute_force(races: &[Race]) -> usize {
    let mut points: usize = 1;
    for race in races {
        let mut wins = 0;
        for i in 0..=race.time as usize {
            let distance = (race.time as usize - i) * i;
            if distance > race.distance as usize {
                wins += 1;
            }
        }
        points *= wins;
    }
    points
}

fn part_1(races: &[Race]) -> usize {
    solve(races)
}

fn part_2(races: &[Race]) -> usize {
    solve(races)
}

fn solve(races: &[Race]) -> usize {
    races.iter().map(solve_quadratic).product()
}

fn solve_quadratic(race: &Race) -> usize {
    let discriminant = race.time.powi(2) - 4.0 * race.distance;
    let solution1 = (-race.time + discriminant.sqrt()) / (-2.0);
    let solution2 = (-race.time - discriminant.sqrt()) / (-2.0);
    ((solution2 - 1.0).ceil() - (solution1 + 1.0).floor()) as usize + 1
}

fn main() {
    let input = include_str!("../../../inputs/input_06.txt");
    let (races, race2) = parse_input(input).unwrap();
    println!("Part 1: {}", part_1(&races));
    println!("Part 2: {}", part_2(&race2));
}

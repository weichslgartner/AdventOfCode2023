use anyhow::{anyhow, Context, Result};

use std::collections::{HashMap, HashSet};
use std::iter::FromIterator;

fn parse_input(input: &str) -> Result<HashMap<usize, usize>> {
    let mut scratchcards = HashMap::new();
    for line in input.lines() {
        let (tmp, yours) = line.split_once('|').context("Failed to split input")?;
        let (id_str, winning) = tmp.split_once(':').context("Failed to split input")?;
        let id: usize = *extract_all_ints(id_str)?
            .first()
            .ok_or(anyhow!("Failed to extract ID"))?;
        let winning_numbers = HashSet::<_>::from_iter(
            extract_all_ints(winning).context("Failed to extract winning numbers")?,
        );
        let yours_numbers = HashSet::<_>::from_iter(
            extract_all_ints(yours).context("Failed to extract your numbers")?,
        );
        scratchcards.insert(id, (winning_numbers.intersection(&yours_numbers)).count());
    }
    Ok(scratchcards)
}

fn part_1(scratchcards: impl Iterator<Item = usize>) -> usize {
    scratchcards
        .filter(|&x| x > 0)
        .map(|x| 2_usize.pow((x - 1) as u32))
        .sum()
}

fn part_2(scratchcards: HashMap<usize, usize>) -> usize {
    let mut stack = Vec::from_iter(scratchcards.clone());
    let mut points = 0;
    while !stack.is_empty() {
        let (id, num_winning) = stack.pop().unwrap();
        points += 1;
        if num_winning > 0 {
            for i in 1..=num_winning {
                stack.push((id + i, scratchcards[&(id + i)]));
            }
        }
    }
    points
}

fn extract_all_ints(s: &str) -> Result<Vec<usize>> {
    let mut result: Vec<_> = Vec::new();
    for cap in regex::Regex::new(r"(\d+)").unwrap().captures_iter(s) {
        result.push(cap[1].parse::<usize>().context("Failed to parse integer")?);
    }
    Ok(result)
}

fn main() {
    let lines = include_str!("../../../inputs/input_04.txt");
    let scratchcards = parse_input(lines).unwrap();
    println!("Part 1: {}", part_1(scratchcards.values().copied()));
    println!("Part 2: {}", part_2(scratchcards));
}

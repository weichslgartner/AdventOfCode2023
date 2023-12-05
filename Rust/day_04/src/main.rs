use anyhow::{Context, Result, anyhow};


use std::collections::HashSet;
use std::iter::FromIterator;

fn parse_input(input: &str) -> Result<Vec<(usize, usize)>> {
    let mut scratchcards = Vec::new();
    for line in input.lines() {
        let (tmp, yours) = line.split_once('|').context("Failed to split input")?;
        let (id_str, winning) = tmp.split_once(':').context("Failed to split input")?;
        let id: usize = *id_str.split(' ').flat_map(|x| x.parse()).collect::<Vec<_>>().last().ok_or(anyhow!("Failed parsing id"))?;
        let winning_numbers = HashSet::<usize>::from_iter(
            winning.trim().split(' ').flat_map(|x| x.trim().parse())
        );
        let yours_numbers = HashSet::<usize>::from_iter(
            yours.trim().split(' ').flat_map(|x| x.trim().parse())
        );
        scratchcards.push((id, (winning_numbers.intersection(&yours_numbers)).count()));
    }
    Ok(scratchcards)
}

fn part_1(scratchcards: &[(usize, usize)]) -> usize {
    scratchcards
        .iter()
        .map(|(_, winning)| winning)
        .filter(|x| *x > &0)
        .map(|x| 2_usize.pow((x - 1) as u32))
        .sum()
}

fn part_2(scratchcards: &[(usize, usize)]) -> usize {
    let mut cards = vec![1; scratchcards.len()];
    for (id, num_winning) in scratchcards.iter() {
        for i in 1..(*num_winning + 1) {
            cards[id - 1 + i] += cards[id - 1];
        }
    }
    cards.iter().sum()
}

fn main() {
    let lines = include_str!("../../../inputs/input_04.txt");
    let scratchcards = parse_input(lines).unwrap();
    println!("Part 1: {}", part_1(&scratchcards));
    println!("Part 2: {}", part_2(&scratchcards));
}



use std::collections::{HashMap, HashSet};
use std::cmp::Ordering;

#[derive(Debug)]
struct Hand {
    hand: String,
    hand_count: HashMap<char, usize>,
    bid: i32,
}

impl Hand {
    fn new(hand: &str, bid: &str) -> Self {
        let hand_count: HashMap<char, usize> = hand.chars().fold(HashMap::new(), |mut acc, c| {
            *acc.entry(c).or_insert(0) += 1;
            acc
        });

        Hand {
            hand: hand.to_string(),
            hand_count,
            bid: bid.parse().unwrap(),
        }
    }
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
enum HandRank {
    FIVES = 6,
    FOURS = 5,
    FULL_HOUSE = 4,
    THREES = 3,
    TWO_PAIRS = 2,
    PAIR = 1,
    HIGHEST_CARD = 0,
}

fn parse_input(input: &str) -> Vec<Hand> {
    input.lines().map(|line| {
        let parts: Vec<&str> = line.split_whitespace().collect();
        Hand::new(parts[0], parts[1])
    }).collect()
}

fn get_highest(hand: &HashMap<char, usize>, part2: bool) -> HandRank {
    let m = hand.iter().max_by(|(_, &count1), (_, &count2)| count1.cmp(count2));
    let most_com = m.unwrap().1;
    let sec_com = hand.iter().nth(1).map(|(_, &count)| count).unwrap_or(0);

    if hand.contains_key(&'J') && part2 {
        substitute_jokers(hand, *most_com)
    } else {
        match (most_com, sec_com) {
            (5, _) => HandRank::FIVES,
            (4, _) => HandRank::FOURS,
            (3, 2) => HandRank::FULL_HOUSE,
            (3, _) => HandRank::THREES,
            (2, 2) => HandRank::TWO_PAIRS,
            (2, _) => HandRank::PAIR,
            _ => HandRank::HIGHEST_CARD,
        }
    }
}

fn substitute_jokers(hand: &HashMap<char, usize>, &most_com: usize) -> HandRank {
    for (card, count) in hand {
        if card != &'J' {
            return HandRank::from(count + hand[&'J']);
        }
    }
    HandRank::from(most_com)
}

fn cmp(c1: &Hand, c2: &Hand, part2: bool) -> Ordering {
    let val_1 = get_highest(&c1.hand_count, part2);
    let val_2 = get_highest(&c2.hand_count, part2);

    if val_1 != val_2 {
        val_1.cmp(&val_2)
    } else if part2 {
        compare_by_card_part(c1, c2, &order_dict2)
    } else {
        compare_by_card_part(c1, c2, &order_dict1)
    }
}

fn compare_by_card_part(c1: &Hand, c2: &Hand, order_dict: &HashMap<char, usize>) -> Ordering {
    for (i1, i2) in c1.hand.chars().zip(c2.hand.chars()) {
        if order_dict[&i1] < order_dict[&i2] {
            return Ordering::Less;
        } else if order_dict[&i1] > order_dict[&i2] {
            return Ordering::Greater;
        }
    }
    Ordering::Equal
}

fn total_winnings(hand_bids: &mut Vec<Hand>, cmp_fun: fn(&Hand, &Hand, bool) -> Ordering) -> i32 {
    hand_bids.sort_by(|c1, c2| cmp_fun(c1, c2, true));
    hand_bids.iter().enumerate().map(|(i, h)| (i as i32 + 1) * h.bid).sum()
}

fn part_1(hand_bids: &mut Vec<Hand>) -> i32 {
    total_winnings(hand_bids, cmp)
}

fn part_2(hand_bids: &mut Vec<Hand>) -> i32 {
    total_winnings(hand_bids, cmp)
}

fn main() {
    let input = include_str!("../../../inputs/input_07.txt");
    let mut hand_bids = parse_input(input);
    println!("Part 1: {}", part_1(&mut hand_bids));
    println!("Part 2: {}", part_2(&mut hand_bids));
}


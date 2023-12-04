use std::collections::{HashMap, HashSet};

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
struct Point {
    x: usize,
    y: usize,
}

impl Point {
    fn new(x: usize, y: usize) -> Point {
        Point { x, y }
    }
}

fn parse_input(lines: Vec<&str>) -> (HashMap<Point, String>, HashMap<Point, char>) {
    let mut num = String::new();
    let mut p: Option<Point> = None;
    let mut nums = HashMap::new();
    let mut symbols = HashMap::new();

    for (y, line) in lines.iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            match c {
                '0'..='9' => {
                    if num.is_empty() {
                        p = Some(Point::new(x, y));
                    }
                    num.push(c);
                }
                '.' => {
                    if !num.is_empty() {
                        nums.insert(p.unwrap(), num.clone());
                        num.clear();
                    }
                }
                _ => {
                    if !num.is_empty() {
                        nums.insert(p.unwrap(), num.clone());
                        num.clear();
                    }
                    symbols.insert(Point::new(x, y), c);
                }
            }
        }
    }

    (nums, symbols)
}

fn has_sym_neighbor(p: Point, length: usize, symbols: &HashMap<Point, char>) -> bool {
    (p.y as isize - 1..=p.y as isize + 1).any(|y| {
        (p.x as isize - 1..=p.x as isize + length as isize)
            .any(|x| symbols.contains_key(&Point::new(x as usize, y as usize)))
    })
}

fn part_1(nums: &HashMap<Point, String>, symbols: &HashMap<Point, char>) -> usize {
    nums.iter()
        .filter(|&(p, numb)| has_sym_neighbor(*p, numb.len(), symbols))
        .map(|(_, numb)| numb.parse::<usize>().unwrap())
        .sum()
}

fn get_gear(p: Point, nums: &HashMap<Point, String>) -> Option<usize> {
    let gear: HashSet<_> = (p.y as isize - 1..=p.y as isize + 1)
        .flat_map(|y| {
            (p.x as isize - 1..=p.x as isize + 1).map(move |x| Point::new(x as usize, y as usize))
        })
        .filter_map(|n| nums.get(&n))
        .map(|num| num.parse::<usize>().unwrap())
        .collect();
    (gear.len() == 2).then_some(gear.iter().product())
}

fn part_2(nums: &HashMap<Point, String>, symbols: &HashMap<Point, char>) -> usize {
    let nums2 = expand_nums(nums);
    symbols
        .iter()
        .filter(|&(_, &c)| c == '*')
        .flat_map(|(&p, _)| get_gear(p, &nums2))
        .sum()
}

fn expand_nums(nums: &HashMap<Point, String>) -> HashMap<Point, String> {
    let mut nums2 = HashMap::new();
    for (p, v) in nums.iter() {
        for i in 0..v.len() {
            nums2.insert(Point::new(p.x + i, p.y), v.clone());
        }
    }
    nums2
}

fn main() {
    let lines: Vec<&str> = include_str!("../../../inputs/input_03.txt")
        .lines()
        .collect();
    let (nums, symbols) = parse_input(lines);
    println!("Part 1: {}", part_1(&nums, &symbols));
    println!("Part 2: {}", part_2(&nums, &symbols));
}

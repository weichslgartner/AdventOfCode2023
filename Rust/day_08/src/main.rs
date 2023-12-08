use num::integer::lcm;
use std::collections::HashMap;

#[derive(Debug)]
struct Node<'a> {
    name: &'a str,
    left: &'a str,
    right: &'a str,
}

fn parse_input(input_str: &str) -> (&str, HashMap<&str, Node>) {
    let (directions, nodes_raw) = input_str.split_once("\n\n").unwrap();
    let nodes_raw = nodes_raw;
    let mut node_dict = HashMap::new();

    for node_raw in nodes_raw.lines() {
        let matches: Vec<_> = node_raw
            .split(|c: char| !c.is_alphanumeric())
            .filter(|s| !s.is_empty())
            .collect();
        let node = Node {
            name: matches[0],
            left: matches[1],
            right: matches[2],
        };
        node_dict.insert(node.name, node);
    }

    (directions, node_dict)
}

fn part_1(directions: &str, node_dict: &HashMap<&str, Node>) -> usize {
    let cur = node_dict.get("AAA").unwrap();
    calc_steps(cur, directions, node_dict, "ZZZ")
}

fn calc_steps<'a>(
    init_node: &Node,
    directions: &str,
    node_dict: &'a HashMap<&'a str, Node<'_>>,
    end_pattern: &str,
) -> usize {
    let mut cur = init_node;
    let mut steps = 0;
    while !cur.name.ends_with(end_pattern) {
        for d in directions.chars() {
            if d == 'L' {
                cur = node_dict.get(&cur.left).unwrap();
            } else {
                cur = node_dict.get(&cur.right).unwrap();
            }
            steps += 1;
        }
    }
    steps
}

fn part_2(directions: &str, node_dict: &HashMap<&str, Node>) -> usize {
    let cur: Vec<&Node> = node_dict
        .iter()
        .filter(|(k, _)| k.ends_with('A'))
        .map(|(_, v)| v)
        .collect();

    cur.iter().fold(1, |acc, &c| {
        lcm(acc, calc_steps(c, directions, node_dict, "Z"))
    })
}

fn main() {
    let input_str = include_str!("../../../inputs/input_08.txt");
    let (directions, node_dict) = parse_input(input_str);
    println!("Part 1: {}", part_1(directions, &node_dict));
    println!("Part 2: {}", part_2(directions, &node_dict));
}

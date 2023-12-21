use std::collections::{HashMap, HashSet};

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
struct Point {
    x: i64,
    y: i64,
}

impl Point {
    fn new(x: i64, y: i64) -> Self {
        Point { x, y }
    }
}

fn get_neighbours_4(p: Point) -> Vec<Point> {
    vec![
        Point::new(p.x-1, p.y),
        Point::new(p.x, p.y-1),
        Point::new(p.x + 1, p.y),
        Point::new(p.x, p.y + 1),
    ]
}

fn parse_input(lines: Vec<&str>) -> (HashSet<Point>, Point, Point) {
    let mut rocks = HashSet::new();
    let mut rocks_row = HashMap::new();
    let mut start = None;
    let mut max_p = Point::new(0, 0);

    for (y, line) in lines.iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            let point = Point::new(x as i64, y as i64);
            match c {
                '#' => {
                    rocks.insert(point);
                    rocks_row.entry(y).or_insert_with(Vec::new).push(point);
                }
                'S' => {
                    start = Some(point);
                }
                _ => {}
            }
        }
        max_p.x = max_p.x.max(lines[y].len() as i64);
    }

    let start = start.expect("Start point not found");
    (rocks, start, Point::new(max_p.x, lines.len() as i64))
}

fn modulo(n: i64, m: i64) -> i64 {
    ((n % m) + m) % m
}

fn is_rock(p: Point, max_p: Point, rocks: &HashSet<Point>) -> bool {
    let y = modulo(p.y, max_p.y);
    let x = modulo(p.x, max_p.x);
    rocks.contains(&Point::new(x,y))
}

fn get_pu(p: Point, max_p: Point) -> Point {
    let y = p.y / max_p.y;
    let x = p.x / max_p.x;
    
    Point::new(x,y)
}

fn part_2(rocks: &HashSet<Point>, start: Point, max_p: Point, steps: usize) -> usize {
    let mut queue = HashSet::<Point>::new();
    let mut pus = HashSet::<Point>::new();
    let mut next_queue = HashSet::<Point>::new();
    let mut next_pus = HashSet::<Point>::new();

    queue.insert(start);

    for i in 0..steps {
        println!("{},{}",i, queue.len());
        for p in &queue {
            for n in get_neighbours_4(*p) {
                if !is_rock(n, max_p, rocks) {
                    next_queue.insert(n);
                }
            }
        }
        queue.clear();
        std::mem::swap(&mut queue, &mut next_queue);
    }

    queue.len()
}

fn main() {
    let lines: Vec<&str> = include_str!("../../../inputs/input_21_test.txt").lines().collect();

 
    let (rocks, start, max_p) = parse_input(lines);
    println!("Part 2: {}", part_2(&rocks, start, max_p, 1000));
}



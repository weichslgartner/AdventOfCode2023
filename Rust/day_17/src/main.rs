use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Element {
    dist: usize,
    p: Point,
    dirs: String,
    heat_loss: usize,
    from: Point,
}

impl Ord for Element {
    fn cmp(&self, other: &Self) -> Ordering {
        other.dist.cmp(&self.dist) // Reverse ordering for min heap
    }
}

impl PartialOrd for Element {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn parse_input(input: &str) -> Vec<Vec<usize>> {
    input
        .lines()
        .map(|line| {
            line.chars()
                .map(|c| c.to_digit(10).unwrap() as usize)
                .collect()
        })
        .collect()
}

fn get_neighbours_4(p: Point, max_p: Point) -> Vec<Point> {
    let mut neighbours = Vec::new();
    if p.x > 0 {
        neighbours.push(Point { x: p.x - 1, y: p.y });
    }
    if p.y > 0 {
        neighbours.push(Point { x: p.x, y: p.y - 1 });
    }
    if p.x < max_p.x - 1 {
        neighbours.push(Point { x: p.x + 1, y: p.y });
    }
    if p.y < max_p.y - 1 {
        neighbours.push(Point { x: p.x, y: p.y + 1 });
    }
    neighbours
}

fn point_to_dir(diff_p: Point) -> char {
    match (diff_p.x, diff_p.y) {
        (-1, 0) => '<',
        (1, 0) => '>',
        (0, -1) => '^',
        (0, 1) => 'v',
        _ => panic!("Invalid direction"),
    }
}

fn manhattan_distance(p1: Point, p2: Point) -> usize {
    ((p1.x - p2.x).abs() + (p1.y - p2.y).abs()) as usize
}

fn count_end_chars(s: &str) -> usize {
    s.chars().rev().take_while(|&c| s.ends_with(c)).count()
}

fn solve(grid: &Vec<Vec<usize>>, start: Point, max_len: usize, min_len: usize) -> usize {
    let max_p = Point {
        x: grid[0].len() as i32,
        y: grid.len() as i32,
    };
    let target = Point {
        x: max_p.x - 1,
        y: max_p.y - 1,
    };
    let mut min_dist = usize::MAX;
    let mut queue = BinaryHeap::new();
    queue.push(Element {
        dist: manhattan_distance(start, target),
        p: start,
        dirs: String::new(),
        heat_loss: 0,
        from: Point { x: 0, y: 0 },
    });
    let mut visited = HashMap::new();

    while let Some(el) = queue.pop() {
        if target == el.p && el.heat_loss <= min_dist {
            if count_end_chars(&el.dirs) < min_len {
                continue;
            }
            min_dist = el.heat_loss;
            continue;
        }

        if el.heat_loss > min_dist {
            continue;
        }
        for n in get_neighbours_4(el.p, max_p) {
            if n == el.from {
                continue;
            }
            let diff_p = Point {
                x: n.x - el.p.x,
                y: n.y - el.p.y,
            };
            let d = point_to_dir(diff_p);
            let new_dirs = if el.dirs.len() > max_len - 1 {
                if el.dirs.chars().take(max_len).all(|c| c == d) {
                    continue;
                }
                el.dirs
                    .chars()
                    .skip(el.dirs.len() - (max_len - 1))
                    .collect::<String>()
                    + &d.to_string()
            } else {
                el.dirs.clone() + &d.to_string()
            };
            if count_end_chars(&el.dirs) < min_len
                && !el.dirs.is_empty()
                && el.dirs.chars().last().unwrap() != d
            {
                continue;
            }
            let cur_heat = el.heat_loss + grid[n.y as usize][n.x as usize];
            if visited
                .get(&(n, new_dirs.clone()))
                .map_or(true, |&v| v > cur_heat)
            {
                visited.insert((n, new_dirs.clone()), cur_heat);
                queue.push(Element {
                    dist: manhattan_distance(n, target) + cur_heat,
                    p: n,
                    dirs: new_dirs.clone(),
                    heat_loss: cur_heat,
                    from: el.p,
                });
            }
        }
    }

    min_dist
}

fn part_1(grid: &Vec<Vec<usize>>, start: Point) -> usize {
    solve(grid, start, 3, 1)
}

fn part_2(grid: &Vec<Vec<usize>>, start: Point) -> usize {
    solve(grid, start, 10, 4)
}

fn main() {
    let input = include_str!("../../../inputs/input_17.txt");
    let grid: Vec<Vec<usize>> = parse_input(input);
    let start = Point { x: 0, y: 0 };
    println!("Part 1: {}", part_1(&grid, start));
    println!("Part 2: {}", part_2(&grid, start));
}

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
    from: Point
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
    match (diff_p.x as i64, diff_p.y as i64) {
        (-1, 0) => '<',
        (1, 0) => '>',
        (0, -1) => '^',
        (0, 1) => 'v',
        _ => panic!("Invalid direction"),
    }
}

fn manhattan_distance(p1: Point, p2: Point) -> usize {
    ((p1.x as isize - p2.x as isize).abs() + (p1.y as isize - p2.y as isize).abs()) as usize
}

fn dir_to_point(c: char) -> Point {
    match c {
        '<' => Point { x: -1, y: 0 },
        '>' => Point { x: 1, y: 0 },
        '^' => Point { x: 0, y: -1 },
        'v' => Point { x: 0, y: 1 },
        _ => panic!("Invalid direction"),
    }
}

fn part_1(grid: Vec<Vec<usize>>, start: Point) -> (usize, String) {
    let max_p = Point {
        x: grid[0].len() as i32,
        y: grid.len() as i32,
    };
    let target = Point {
        x: max_p.x - 1,
        y: max_p.y - 1,
    };
    let mut min_dist = usize::MAX;
    let mut res = String::new();
    let mut queue = BinaryHeap::new();
    queue.push(Element {
        dist: manhattan_distance(start, target),
        p: start,
        dirs: String::new(),
        heat_loss: 0,
        from: Point{x:0,y:0}
    });
    let mut visited = HashMap::new();

    while let Some(el) = queue.pop() {
        if target == el.p && el.heat_loss <= min_dist {
            min_dist = el.heat_loss;
            res = el.dirs.clone();
            continue;
        }

        if el.heat_loss > min_dist {
            continue;
        }

        let ns = get_neighbours_4(el.p, max_p);
        for n in ns {
            if n == el.from{
                continue
            }
            let diff_p = Point {
                x: n.x as i32 - el.p.x as i32,
                y: n.y as i32 - el.p.y as i32,
            };
            let d = point_to_dir(diff_p);
            let new_dirs = if el.dirs.len() > 2 {
                if el.dirs.chars().take(3).all(|c| c == d) {
                    continue;
                }
                el.dirs.chars().skip(el.dirs.len() - 2).collect::<String>() + &d.to_string()
            } else {
                el.dirs.clone() + &d.to_string()
            };
            assert!(el.dirs.len() <=3);
            if new_dirs
                .chars()
                .skip(new_dirs.len() - 2)
                .collect::<String>()
                == "<>"
                || new_dirs
                    .chars()
                    .skip(new_dirs.len() - 2)
                    .collect::<String>()
                    == "v^"
            {
                continue;
            }

            if visited.get(&(n, new_dirs.clone())).map_or(true, |&v| {
                v > el.heat_loss + grid[n.y as usize][n.x as usize]
            }) {
                visited.insert(
                    (n, new_dirs.clone()),
                    el.heat_loss + grid[n.y as usize][n.x as usize],
                );
                queue.push(Element {
                    dist: manhattan_distance(n, target)+el.heat_loss + grid[n.y as usize][n.x as usize],
                    p: n,
                    dirs: new_dirs.clone(),
                    heat_loss: el.heat_loss + grid[n.y as usize][n.x as usize],
                    from: el.p
                });
            }
        }
    }

    (min_dist, res)
}

fn part_2(lines: Vec<&str>) {
    // Implement part 2 logic here
}

fn main() {
    let input = include_str!("../../../inputs/input_17.txt");
    let grid: Vec<Vec<usize>> = parse_input(input);
    let start = Point { x: 0, y: 0 };
    let (part1, res) = part_1(grid, start);
    println!("Part 1: {}", part1);
    //  println!("Part 2: {}", part_2(&input));
}

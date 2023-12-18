use std::fmt;

#[derive(Debug, Copy, Clone, PartialEq, Eq, Hash)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
enum Dir {
    Right,
    Down,
    Left,
    Up,
}

impl Dir {
    fn from_char(c: char) -> Option<Dir> {
        match c {
            'R' => Some(Dir::Right),
            'D' => Some(Dir::Down),
            'L' => Some(Dir::Left),
            'U' => Some(Dir::Up),
            _ => None,
        }
    }
}

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
struct Trench {
    dir: Dir,
    len: usize,
}

impl fmt::Display for Trench {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:?} {}", self.dir, self.len)
    }
}

fn parse_input(input: &str) -> Vec<(Trench, Trench)> {
    input
        .lines()
        .map(|line| {
            let parts: Vec<&str> = line.split_whitespace().collect();
            let d = Dir::from_char(parts[0].chars().next().unwrap()).unwrap();
            let l = parts[1].parse().unwrap();
            let c = parts[2].trim();
            //println!{"{}",u32::from_str_radix(&c[2..c.len() - 2], 16).unwrap()};
            (
                Trench { dir: d, len: l },
                Trench {
                    dir: hex_to_dir(c.chars().nth(c.len() - 2).unwrap()),
                    len: u32::from_str_radix(&c[2..c.len() - 2], 16).unwrap() as usize,
                },
            )
        })
        .collect()
}

fn hex_to_dir(c: char) -> Dir {
    match c {
        '0' => Dir::Right,
        '1' => Dir::Down,
        '2' => Dir::Left,
        '3' => Dir::Up,
        _ => panic!("Invalid hex value"),
    }
}

fn create_polygon(trenches: &Vec<Trench>) -> (usize, Vec<Point>) {
    trenches.iter().fold(
        (0, vec![Point { x: 0, y: 0 }]),
        |(mut acc_perim, mut acc_polygon), trench| {
            let dp = match trench.dir {
                Dir::Right => Point { x: 1, y: 0 },
                Dir::Down => Point { x: 0, y: 1 },
                Dir::Left => Point { x: -1, y: 0 },
                Dir::Up => Point { x: 0, y: -1 },
            };

            let new_point = Point {
                x: acc_polygon.last().unwrap().x + dp.x * trench.len as i32,
                y: acc_polygon.last().unwrap().y + dp.y * trench.len as i32,
            };

            acc_perim += trench.len;
            acc_polygon.push(new_point);

            (acc_perim, acc_polygon)
        },
    )
}

fn calc_area(perim: usize, polygon: Vec<Point>) -> u128 {
    (polygon
        .windows(2)
        .map(|pair| (pair[0].x * pair[1].y - pair[0].y * pair[1].x) as u128)
        .sum::<u128>()
        / 2
        + (perim / 2) as u128)
        + 1
}

fn solve(trenches: &Vec<Trench>) -> u128 {
    let (perim, polygon) = create_polygon(&trenches);
    calc_area(perim, polygon)
}

fn part_1(trenches: &Vec<(Trench, Trench)>) -> u128 {
    solve(&trenches.iter().map(|(t, _)| *t).collect())
}

fn part_2(trenches: &Vec<(Trench, Trench)>) -> u128 {
    solve(&trenches.iter().map(|(_, t)| *t).collect())
}

fn main() {
    let input = include_str!("../../../inputs/input_18.txt");
    let trenches = parse_input(&input);
    println!("Part 1: {}", part_1(&trenches));
    println!("Part 2: {}", part_2(&trenches));
}

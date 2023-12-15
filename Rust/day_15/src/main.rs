#[derive(Clone, Debug)]
struct Lens<'a> {
    label: &'a str,
    focal: u8,
}

fn part_1(input: &str) -> usize {
    input.split(',').map(aoc_hash).sum()
}

fn aoc_hash(x: &str) -> usize {
    x.chars()
        .fold(0, |accu, c| (accu + u64::from(c)) * 17 % 256) as usize
}

fn part_2(input: &str) -> usize {
    let mut vec: Vec<Vec<Lens>> = vec![vec![]; 256];
    input.split(',').for_each(|s| {
        if s.contains('=') {
            let (label, focal) = s.split_once('=').unwrap();
            let idx = aoc_hash(label);
            let lens = Lens {
                label,
                focal: focal.parse().unwrap(),
            };
            let same_label_idx = vec[idx].iter().position(|x| lens.label == x.label);
            if let Some(i) = same_label_idx {
                vec[idx][i] = lens;
            } else {
                vec[idx].push(lens);
            }

        } else {
            let (label, _) = s.split_once('-').unwrap();
            let idx = aoc_hash(label);
            let same_label_idx = vec[idx].iter().position(|x| label == x.label);
            if let Some(i) = same_label_idx {
                vec[idx].remove(i);
            }
        }
    });

    focus_power(vec)
}

fn focus_power(vec: Vec<Vec<Lens<'_>>>) -> usize {
    vec.iter()
        .enumerate()
        .map(|(box_n, content)| -> usize {
            (box_n + 1)
                * content
                    .iter()
                    .enumerate()
                    .map(|(pos, lenses)| (pos + 1) * lenses.focal as usize)
                    .sum::<usize>()
        })
        .sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_15.txt");
    println!("Part 1: {}", part_1(input));
    println!("Part 2: {}", part_2(input));
}

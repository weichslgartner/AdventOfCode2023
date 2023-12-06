use itertools::Itertools;
use rayon::prelude::*;

#[derive(Debug, Copy, Clone)]
struct CMap {
    begin: usize,
    end: usize,
    target: usize,
}

impl CMap {
    fn new(begin: usize, end: usize, target: usize) -> Self {
        CMap { begin, end, target }
    }
}

#[derive(Debug, Copy, Clone)]
struct Interval {
    begin: usize,
    end: usize,
}

impl Interval {
    fn new(begin: usize, end: usize) -> Self {
        Interval { begin, end }
    }
}

fn parse_input(input_str: &str) -> (Vec<usize>, Vec<Vec<CMap>>) {
    let mut all_maps = Vec::new();
    let mut seeds = Vec::new();
    let mut translation_maps = Vec::new();

    for (i, block) in input_str.split("\n\n").enumerate() {
        for line in block.split('\n') {
            let ints: Vec<usize> = line.split_whitespace().flat_map(|s| s.parse()).collect();
            if i == 0 {
                seeds = ints;
            } else if ints.is_empty() {
                sort_and_push(translation_maps, &mut all_maps);
                translation_maps = Vec::new();
                continue;
            } else {
                translation_maps.push(CMap::new(ints[1], ints[1] + ints[2] - 1, ints[0]));
            }
        }
    }
    sort_and_push(translation_maps, &mut all_maps);
    (seeds, all_maps)
}

fn sort_and_push(mut translation_maps: Vec<CMap>, all_maps: &mut Vec<Vec<CMap>>) {
    if !translation_maps.is_empty() {
        translation_maps.sort_by_key(|x: &CMap| x.begin);
        all_maps.push(translation_maps);
    }
}

fn convert_ranges(interval: Interval, maps: &[CMap]) -> Vec<Interval> {
    let mut target = Vec::new();
    let mut interval = interval;
    for (i, cmap) in maps.iter().enumerate() {
        let next_cmap = maps.get(i + 1);
        assert!(interval.begin <= interval.end);
        // left overlap
        if cmap.end >= interval.begin && interval.begin >= cmap.begin {
            // complete overlap
            if cmap.end >= interval.end {
                target.push(Interval::new(
                    cmap.target + interval.begin - cmap.begin,
                    cmap.target + interval.end - cmap.begin,
                ));
                return target;
            // partial overlap
            } else {
                target.push(Interval::new(
                    cmap.target + interval.begin - cmap.begin,
                    cmap.target + cmap.end - cmap.begin,
                ));
                interval.begin = cmap.end + 1;
            }
        }
        // right side overlaps
        else if cmap.begin <= interval.end && interval.end <= cmap.end {
            target.push(Interval::new(
                cmap.target,
                cmap.target + interval.end - cmap.begin,
            ));
            target.push(Interval::new(interval.begin, cmap.begin - 1));
            return target;
        }
        // cmap is included in interval
        else if cmap.begin >= interval.begin && cmap.end <= interval.end {
            target.push(Interval::new(
                cmap.target,
                cmap.target + cmap.end - cmap.begin,
            ));
            if interval.begin < cmap.begin {
                target.push(Interval::new(interval.begin, cmap.begin - 1));
                interval = Interval::new(cmap.end + 1, interval.end);
            }
        }
        // no overlap
        else if let Some(next_cmap) = next_cmap {
            if interval.end < next_cmap.begin {
                target.push(interval);
                return target;
            }
        // finished
        } else {
            target.push(interval);
            return target;
        }
    }
    target.push(interval);
    if target.is_empty() {
        vec![interval]
    } else {
        target
    }
}

fn binary_search(location: usize, maps: &[CMap]) -> usize {
    let mut low = 0;
    let mut high = maps.len() - 1;
    while low <= high {
        let m = (low + high) / 2;
        let cmap = &maps[m];

        if cmap.begin <= location && location <= cmap.end {
            return cmap.target + location - cmap.begin;
        }
        if cmap.end < location {
            low = m + 1;
        } else if cmap.begin > location {
            if m == 0 {
                return location;
            }
            high = m - 1;
        }
    }
    location
}

fn part_1(seeds: &[usize], all_maps: &[Vec<CMap>]) -> usize {
    seeds
        .iter()
        .map(|seed| transform_seed(all_maps, seed))
        .min()
        .unwrap()
}

fn transform_seed(all_maps: &[Vec<CMap>], seed: &usize) -> usize {
    all_maps
        .iter()
        .fold(*seed, |location, stage| binary_search(location, stage))
}


fn part_2(seeds_raw: &[usize], all_maps: &[Vec<CMap>]) -> Option<usize> {
    seeds_raw
        .iter()
        .tuples()
        .flat_map(|(&seed_begin, &width)| min_per_seed_range(all_maps, seed_begin, width))
        .min()
}

fn min_per_seed_range(all_maps: &[Vec<CMap>], seed_begin: usize, width: usize) -> Option<usize> {
    all_maps
        .iter()
        .fold(
            vec![Interval::new(seed_begin, seed_begin + width - 1)],
            |acc_intervals, stage| {
                acc_intervals
                    .iter()
                    .flat_map(|interval| convert_ranges(*interval, stage))
                    .collect()
            },
        )
        .iter()
        .map(|x| x.begin)
        .min()
}

fn main() {
    let input = include_str!("../../../inputs/input_05.txt");
    let (seeds, all_maps) = parse_input(input);
    println!("Part 1: {}", part_1(&seeds, &all_maps));
    if cfg!(feature = "brute-force"){
        println!("Part 2: {}", brute_force(&seeds, &all_maps).unwrap()); //brute force version takes
    }else{
        println!("Part 2: {}", part_2(&seeds, &all_maps).unwrap());
    }
    //
}


fn brute_force(seeds_raw: &[usize], all_maps: &[Vec<CMap>]) -> Option<usize> {
    let ranges: Vec<(&usize, &usize)> = seeds_raw.iter().tuples().collect();
    ranges
        .par_iter()
        .flat_map(|(&start, &length)| {
            (start..=start + length)
                .map(|seed| transform_seed(all_maps, &seed))
                .min()
        })
        .min()
}
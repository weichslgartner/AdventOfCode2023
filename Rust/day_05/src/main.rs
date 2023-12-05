use std::cmp;

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
            let ints: Vec<usize> = line
                .split_whitespace()
                .filter_map(|s| s.parse().ok())
                .collect();
            if i == 0 {
                seeds = ints;
            } else if ints.is_empty() {
                if !translation_maps.is_empty() {
                    translation_maps.sort_by_key(|x: &CMap| x.begin);
                    all_maps.push(translation_maps);
                }
                translation_maps = Vec::new();
                continue;
            } else {
                translation_maps.push(CMap::new(ints[1], ints[1] + ints[2] - 1, ints[0]));
            }
        }
    }
    if !translation_maps.is_empty() {
        translation_maps.sort_by_key(|x| x.begin);
        all_maps.push(translation_maps.clone());
    }
    (seeds, all_maps)
}

fn convert_ranges(interval: Interval, maps: &[CMap]) -> Vec<Interval> {
    let mut target = Vec::new();
    let mut interval = interval;
    for (i, cmap) in maps.iter().enumerate() {
        let next_cmap = maps.get(i + 1);
        assert!(interval.begin <= interval.end);
        // left overlap
        if cmap.end >= interval.begin && interval.begin >= cmap.begin {
            if cmap.end >= interval.end {
                target.push(Interval::new(
                    cmap.target + interval.begin - cmap.begin,
                    cmap.target + interval.end - cmap.begin,
                ));
                return target;
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
    let mut best = usize::MAX;

    for &seed in seeds {
        let mut location = seed;
        for stage in all_maps {
            location = binary_search(location, stage);
        }
        best = cmp::min(location, best);
    }
    best
}

fn part_2(seeds_raw: &[usize], all_maps: &[Vec<CMap>]) -> usize {
    let mut best = usize::MAX;

    for seeds in seeds_raw.chunks(2) {
        let seed_begin = seeds[0];
        let width = seeds[1];
        let mut intervals = vec![Interval::new(seed_begin, seed_begin + width - 1)];

        for stage in all_maps {
            let mut new_intervals = Vec::new();

            for interval in &intervals {
                new_intervals.extend(convert_ranges(*interval, stage));
            }

            intervals = new_intervals;
        }

        best = cmp::min(
            intervals
                .iter()
                .map(|x| x.begin)
                .min()
                .unwrap_or(usize::MAX),
            best,
        );
    }

    best
}

fn main() {
    let input = include_str!("../../../inputs/input_05.txt");
    let (seeds, all_maps) = parse_input(input);
    println!("Part 1: {}", part_1(&seeds, &all_maps));
    println!("Part 2: {}", part_2(&seeds, &all_maps));
}

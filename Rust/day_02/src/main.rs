use std::collections::HashMap;

fn parse_input(input: &str) -> HashMap<u32, Vec<HashMap<String, u32>>> {
    let mut games = HashMap::new();
    for line in input.lines() {
        let parts: Vec<&str> = line.splitn(2, ':').collect();
        let game_id: u32 = parts[0].splitn(2, ' ').last().unwrap().parse().unwrap();
        let draws: Vec<HashMap<String, u32>> = parts[1]
            .split(';')
            .map(|draw| {
                draw.split(',')
                    .map(|rev_set| {
                        let rev_parts: Vec<&str> = rev_set.splitn(3, ' ').collect();
                        let color = rev_parts[2].to_string();
                        let num: u32 = rev_parts[1].parse().unwrap();
                        (color, num)
                    })
                    .collect::<HashMap<String, u32>>()
            })
            .collect();
        games.insert(game_id, draws);
    }
    games
}

fn is_valid(constraints: &HashMap<String, u32>, game: &Vec<HashMap<String, u32>>) -> bool {
    game.iter().all(|draw| {
        draw.iter()
            .all(|(color, num)| *num <= *constraints.get(color).unwrap())
    })
}

fn part_1(games: &HashMap<u32, Vec<HashMap<String, u32>>>) -> u32 {
    let constraints = [
        ("red".to_string(), 12),
        ("green".to_string(), 13),
        ("blue".to_string(), 14),
    ]
    .iter()
    .cloned()
    .collect::<HashMap<String, u32>>();
    games
        .iter()
        .filter(|(_, game)| is_valid(&constraints, game))
        .map(|(game_id, _)| game_id)
        .sum()
}

fn calc_power(game: &Vec<HashMap<String, u32>>) -> u32 {
    game.iter()
        .flat_map(|draw| draw.iter())
        .fold(HashMap::new(), |mut min_conf, (color, num)| {
            let entry = min_conf.entry(color.clone()).or_insert(0);
            if *entry < *num {
                *entry = *num;
            }
            min_conf
        })
        .values()
        .product()
}

fn part_2(games: &HashMap<u32, Vec<HashMap<String, u32>>>) -> u32 {
    games.values().map(calc_power).sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_02.txt");
    let games = parse_input(input);
    println!("Part 1: {}", part_1(&games));
    println!("Part 2: {}", part_2(&games));
}

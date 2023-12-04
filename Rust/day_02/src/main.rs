use std::collections::HashMap;

use anyhow::{Result, anyhow};

type GameT = Vec<HashMap<String, u32>>;

fn parse_input(input: &str) -> Result<Vec<(u32, GameT)>> {
    let mut games = Vec::new();
    for line in input.lines() {
        let (game_id, parts) = line.split_once(':').ok_or(anyhow!("Invalid input format"))?;
        let game_id: u32 = game_id.splitn(2, ' ').last().ok_or(anyhow!("Invalid game ID format"))?.parse()?;
        let draws: Vec<HashMap<String, u32>> = parts
            .split(';')
            .map(|draw| {
                draw.split(',')
                    .map(|rev_set| {
                        let (num, color) = rev_set.trim().split_once(' ').ok_or(anyhow!("Invalid draw format"))?;
                        Ok((color.to_owned(), num.parse()?))
                    })
                    .collect::<Result<Vec<(String, u32)>>>()
                    .map(|vec| vec.into_iter().collect())
            })
            .collect::<Result<Vec<HashMap<String, u32>>>>()?;

        games.push((game_id, draws));
    }
    Ok(games)
}


fn is_valid(constraints: &HashMap<String, u32>, game: &[HashMap<String, u32>]) -> bool {
    game.iter().all(|draw| {
        draw.iter()
            .all(|(color, num)| *num <= *constraints.get(color).unwrap())
    })
}

fn part_1(games: &[(u32, GameT)]) -> u32 {
    let constraints = [
        ("red".to_string(), 12),
        ("green".to_string(), 13),
        ("blue".to_string(), 14),
    ]
    .into_iter()
    .collect::<HashMap<String, u32>>();
    games
        .iter()
        .filter_map(|(game_id, game)| is_valid(&constraints, game).then_some(game_id))
        .sum()
}

fn calc_power(game: &[HashMap<String, u32>]) -> u32 {
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

fn part_2(games: &[(u32, GameT)]) -> u32 {
    games.iter().map(|(_,game)| calc_power(game)).sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_02.txt");
    let games = parse_input(input).unwrap();
    println!("Part 1: {}", part_1(&games));
    println!("Part 2: {}", part_2(&games));
}

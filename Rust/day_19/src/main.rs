use regex::Regex;
use std::collections::HashMap;

#[derive(Debug)]
struct Rule {
    lhs: Option<String>,
    rhs: Option<i32>,
    compare: Option<char>,
    result: String,
}

//cmp2fun = {"<": lt, ">": gt}
fn cmp(c: char, lhs: i32, rhs: i32) -> bool {
    match c {
        // {">": max, "<": min}
        '>' => lhs > rhs,
        _ => lhs < rhs,
    }
}

fn cmp_negate(c: char) -> char {
    match c {
        '>' => '<',
        '<' => '>',
        _ => panic!("cannot negate this"),
    }
}

fn min_max(c: char, lhs: i32, rhs: i32) -> i32 {
    match c {
        // {">": max, "<": min}
        '>' => lhs.max(rhs),
        _ => lhs.min(rhs),
    }
}

fn cmp_negate_corr(c: char) -> i32 {
    match c {
        '>' => -1,
        '<' => 1,
        _ => panic!("only can negate <>"),
    }
}

fn parse_input(in_str: &str) -> (HashMap<String, Vec<Rule>>, Vec<HashMap<String, i32>>) {
    let mut rules = HashMap::new();
    let mut workflows_parts = in_str.split("\n\n");
    let workflows_str = workflows_parts.next().unwrap();
    let parts_str = workflows_parts.next().unwrap();

    for w in workflows_str.lines() {
        let mut iter = w.splitn(2, '{');
        let name = iter.next().unwrap().to_string();
        let rest = iter.next().unwrap();
        let mut rules_group = Vec::new();

        for group in rest.replace("}", "").split(',') {
            if group.contains('>') {
                rules_group.push(extract_comparison(group, ">"));
            } else if group.contains('<') {
                rules_group.push(extract_comparison(group, "<"));
            } else {
                rules_group.push(Rule {
                    result: group.trim().to_string(),
                    lhs: None,
                    rhs: None,
                    compare: None,
                });
            }
        }
        rules.insert(name, rules_group);
    }

    let mut p_ratings = Vec::new();
    for p in parts_str.lines() {
        let mut ratings = HashMap::new();
        for group in p
            .strip_prefix('{')
            .unwrap_or_default()
            .strip_suffix('}')
            .unwrap_or_default()
            .split(',')
        {
            let mut iter = group.split('=');
            let part = iter.next().unwrap().trim().to_string();
            let rating = iter.next().unwrap().trim().parse().unwrap();
            ratings.insert(part, rating);
        }
        p_ratings.push(ratings);
    }

    (rules, p_ratings)
}

fn extract_comparison(group: &str, comp: &str) -> Rule {
    let re = Regex::new(&format!(r"{}|:", comp)).unwrap();
    let subs: Vec<&str> = re.split(group).collect();
    Rule {
        lhs: Some(subs[0].to_string()),
        rhs: Some(subs[1].parse().unwrap()),
        compare: Some(comp.chars().next().unwrap()),
        result: subs[2].to_string(),
    }
}

fn eval_rule(rule: &Rule, pr: &HashMap<String, i32>) -> bool {
    if rule.lhs.is_none() {
        true
    } else {
        let lhs_val = pr.get(rule.lhs.as_ref().unwrap()).unwrap();
        let rhs_val = rule.rhs.unwrap();
        cmp(rule.compare.unwrap(), *lhs_val, rhs_val)
    }
}

fn chain_eval(pr: &HashMap<String, i32>, rules: &HashMap<String, Vec<Rule>>) -> i32 {
    let mut cur_rules = &rules["in"];
    loop {
        for rule in cur_rules {
            if eval_rule(rule, pr) {
                match rule.result.as_str() {
                    "A" => return pr.values().sum(),
                    "R" => return 0,
                    _ => {
                        cur_rules = &rules[&rule.result];
                        break;
                    }
                }
            }
        }
    }
}

fn calc_combos(constraints: &Vec<HashMap<String, i32>>) -> i128 {
    constraints.iter().map(comb_per_constr).sum()
}

fn comb_per_constr(const_: &HashMap<String, i32>) -> i128 {
    (const_["x<"] - const_["x>"] - 1) as i128
        * (const_["m<"] - const_["m>"] - 1) as i128
        * (const_["a<"] - const_["a>"] - 1) as i128
        * (const_["s<"] - const_["s>"] - 1) as i128
}

fn forward_calc(
    cur_key: &str,
    rules: &HashMap<String, Vec<Rule>>,
    const_: &mut HashMap<String, i32>,
    all_constraints: &mut Vec<HashMap<String, i32>>,
) {
    if cur_key == "A" {
        all_constraints.push(const_.clone());
    } else if cur_key != "R" {
        for r in &rules[cur_key] {
            let mut tmp_const = const_.clone();
            if let Some(compare) = r.compare {
                let lhs_cmp = format!("{}{}", &r.lhs.as_ref().unwrap(), compare);
                let cmp_neg = cmp_negate(compare);
                let lhs_cmp_neg = format!("{}{}", &r.lhs.as_ref().unwrap(), &cmp_neg);
                tmp_const.insert(
                    lhs_cmp.clone(),
                    min_max(compare, tmp_const[&lhs_cmp], r.rhs.unwrap()),
                );
                const_.insert(
                    lhs_cmp_neg.clone(),
                    min_max(cmp_neg, tmp_const[&lhs_cmp_neg], r.rhs.unwrap())
                        + cmp_negate_corr(cmp_neg),
                );
            }
            forward_calc(&r.result, rules, &mut tmp_const, all_constraints); // Pass cmp_negate here
        }
    }
}

fn part_1(rules: &HashMap<String, Vec<Rule>>, p_ratings: &Vec<HashMap<String, i32>>) -> i32 {
    p_ratings.iter().map(|pr| chain_eval(pr, rules)).sum()
}

fn part_2(rules: &HashMap<String, Vec<Rule>>) -> i128 {
    let mut all_constraints = Vec::new();
    let mut constraints = constraints_dict();
    forward_calc("in", rules, &mut constraints, &mut all_constraints);
    calc_combos(&all_constraints)
}

fn constraints_dict() -> HashMap<String, i32> {
    let mut constraints = HashMap::new();
    for char in "xmas".chars() {
        constraints.insert(format!("{}>", char), 0);
        constraints.insert(format!("{}<", char), 4001);
    }
    constraints
}

fn main() {
    let input = include_str!("../../../inputs/input_19.txt");
    let (rules, p_ratings) = parse_input(input);
    println!("Part 1: {}", part_1(&rules, &p_ratings));
    println!("Part 2: {}", part_2(&rules));
}

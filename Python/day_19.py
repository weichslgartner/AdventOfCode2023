import re
import string
from math import prod
from operator import gt, lt
from typing import List, Dict, Tuple

from aoc import input_as_str

cmp2fun = {"<": lt, ">": gt}
cmp_negate = {">": "<", "<": ">"}
cmp_negate_corr = {">": -1, "<": 1}
min_max = {">": max, "<": min}


class Rule:
    def __init__(self, result: str, lhs: str = None, rhs: int = None, compare: str = None):
        self.lhs = lhs
        self.rhs = rhs
        self.compare = compare
        self.result = result

    def __repr__(self) -> str:
        return f"{self.lhs}  {self.compare} {self.rhs} -> {self.result}"


def parse_input(in_str: str) -> Tuple[Dict[str, List[Rule]], List[Dict[str, int]]]:
    workflows_str, parts_str = in_str.split("\n\n", 1)
    return parse_rules(workflows_str), parse_ratings(parts_str)


def parse_ratings(parts_str: str) -> List[Dict]:
    p_ratings = []
    for p in parts_str.split("\n"):
        ratings = {}
        for group in p.strip("{}" + string.whitespace).split(","):
            part, rating = group.split("=", 1)
            ratings[part] = int(rating)
        p_ratings.append(ratings)
    return p_ratings


def parse_rules(workflows_str: str) -> Dict[str, List[Rule]]:
    rules = dict()
    for w in workflows_str.split("\n"):
        name, rest = w.split("{", 1)
        rules_group = []
        for group in rest.replace("}", '').split(","):
            if ">" in group:
                r = extract_comparison(group, ">")
            elif "<" in group:
                r = extract_comparison(group, "<")
            else:
                r = Rule(result=group)
            rules_group.append(r)
        rules[name] = rules_group
    return rules


def extract_comparison(group: str, comp: str = ">") -> Rule:
    subs = re.split(f'{comp}|:', group)
    return Rule(lhs=subs[0], rhs=int(subs[1]), compare=comp, result=subs[2])


def eval_rule(rule: Rule, pr: Dict[str, int]) -> bool:
    if rule.lhs is None:
        return True
    return cmp2fun[rule.compare](pr[rule.lhs], rule.rhs)


def chain_eval(pr: Dict[str, int], rules: Dict[str, List[Rule]]) -> int:
    cur_rules: List[Rule] = rules["in"]
    while True:
        for rule in cur_rules:
            if eval_rule(rule, pr):
                if rule.result == 'A':
                    return sum(pr.values())
                elif rule.result == 'R':
                    return 0
                else:
                    cur_rules = rules[rule.result]
                    break


def calc_combos(constraints: List[Dict[str, int]]) -> int:
    return sum(comb_per_constr(const) for const in constraints)


def comb_per_constr(const: Dict[str, int]) -> int:
    return prod((const[c + "<"] - const[c + ">"] - 1) for c in "xmas")


def forward_calc(cur_key: str, rules: Dict[str, List[Rule]], const: Dict[str, int],
                 all_constraints: List[Dict[str, int]]) -> None:
    if cur_key == "A":
        all_constraints.append(const)
        return
    if cur_key == "R":
        return
    for r in rules[cur_key]:
        tmp_const = const.copy()
        if r.compare is not None:
            tmp_const[r.lhs + r.compare] = min_max[r.compare](tmp_const[r.lhs + r.compare], r.rhs)
            cmp_neg = cmp_negate[r.compare]
            const[r.lhs + cmp_neg] = min_max[cmp_neg](tmp_const[r.lhs + cmp_neg], r.rhs) + cmp_negate_corr[cmp_neg]
        forward_calc(r.result, rules, tmp_const, all_constraints)


def part_1(rules: Dict[str, List[Rule]], p_ratings: List[Dict[str, int]]) -> int:
    return sum(chain_eval(pr, rules) for pr in p_ratings)


def part_2(rules: Dict[str, List[Rule]]) -> int:
    all_constraints = []
    constraints = {f"{char}{comp}": value for char in "xmas" for comp, value in zip((">", "<"), (0, 4001))}
    forward_calc("in", rules, constraints, all_constraints)
    return calc_combos(all_constraints)


def main():
    in_str = input_as_str("input_19.txt")
    rules, p_ratings = parse_input(in_str)
    print("Part 1:", part_1(rules, p_ratings))
    print("Part 2:", part_2(rules))


if __name__ == '__main__':
    main()

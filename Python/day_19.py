import string
from collections import OrderedDict, defaultdict
from operator import gt, lt
from typing import List

from aoc import get_lines, input_as_str
import re

cmp2fun = {"<": lt, ">": gt}

cmp_negate = {">": "<", "<": ">"}

min_max = {">": max, "<": min}


class Rule:
    def __init__(self, result, lhs=None, rhs=None, compare=None):
        self.lhs = lhs
        self.rhs = rhs
        self.compare = compare
        self.result = result

    def __repr__(self):
        return f"{self.lhs}  {self.compare} {self.rhs} -> {self.result}"


def parse_input(in_str):
    rules = dict()
    workflows_str, parts_str = in_str.split("\n\n", 1)
    # px{a<2006:qkq,m>2090:A,rfg}
    re.compile("( ([a-z])([<>])([a-z]+|[AR]))")
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
    p_ratings = []
    for p in parts_str.split("\n"):
        ratings = {}
        for group in p.strip("{}" + string.whitespace).split(","):
            part, rating = group.split("=", 1)
            ratings[part] = int(rating)
        p_ratings.append(ratings)
    return rules, p_ratings


def extract_comparison(group, comp=">"):
    subs = re.split(f'{comp}|:', group)
    r = Rule(lhs=subs[0], rhs=int(subs[1]), compare=comp, result=subs[2])
    return r


def eval_rule(rule: Rule, pr):
    if rule.lhs is None:
        return True
    return cmp2fun[rule.compare](pr[rule.lhs], rule.rhs)


def part_1(rules: OrderedDict, p_ratings):
    accepted = 0
    for pr in p_ratings:
        accepted += chain_eval(pr, rules)
    return accepted


def chain_eval(pr, rules):
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


def get_constraints(cur_key, reverse_list, rules, from_key, const, all_constraints):
    invert_cmp = False
    for r in reversed(rules[cur_key]):
        if invert_cmp:
            cmp_neg = cmp_negate[r.compare]
            const[r.lhs + cmp_neg] = min_max[cmp_neg](const[r.lhs + cmp_neg], r.rhs)
        if r.result == from_key:
            if r.compare is not None:
                const[r.lhs + r.compare] = min_max[r.compare](const[r.lhs + r.compare], r.rhs)
            invert_cmp = True
    if cur_key == "in":
        if is_valid(const):
            all_constraints.append(const)
        #print(const,is_valid(const))
        return
    tmp_const = const.copy()
    for next_key in reverse_list[cur_key]:
        get_constraints(next_key, reverse_list, rules, cur_key, tmp_const, all_constraints)


def is_valid(const):
    for c in "xmas":
        if const[c+">"] >= const[c+"<"]:
            return False
    return True

def part_2(rules):
    constraints = []
    reverse_list = reverse_graph(rules)
    for r in reverse_list["A"]:
        const = {"x>": 0, "x<": 4001,
                 "m>": 0, "m<": 4001,
                 "a>": 0, "a<": 4001,
                 "s>": 0, "s<": 4001
                 }
        get_constraints(r, reverse_list, rules, 'A', const,constraints)

    for const in constraints:
        print(const,is_valid(const))
    print(reverse_list)
    pass


def reverse_graph(rules):
    reverse_list = defaultdict(list)
    for key, val in rules.items():
        for sr in val:
            reverse_list[sr.result].append(key)
    return reverse_list


def main():
    in_str = input_as_str("input_19_test.txt")
    rules, p_ratings = parse_input(in_str)
    print("Part 1:", part_1(rules, p_ratings))
    print("Part 2:", part_2(rules))


if __name__ == '__main__':
    main()

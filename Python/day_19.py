import string
from collections import OrderedDict
from operator import gt, lt
from typing import List

from aoc import get_lines, input_as_str
import re

cmp_dict= {"<": lt, ">" : gt}
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
    #px{a<2006:qkq,m>2090:A,rfg}
    re.compile("( ([a-z])([<>])([a-z]+|[AR]))")
    for w in workflows_str.split("\n"):
        name,rest = w.split("{",1)
        rules_group = []
        for group in rest.replace("}",'').split(","):

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
        ratings={}
        for group in p.strip("{}" + string.whitespace).split(","):
            part,rating = group.split("=",1)
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
    return cmp_dict[rule.compare](pr[rule.lhs],rule.rhs)

def part_1(rules: OrderedDict, p_ratings):
    accepted = 0
    for pr in p_ratings:
        accepted += chain_eval( pr, rules)

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



def part_2(rules, p_ratings):
    pass


def main():
    in_str = input_as_str("input_19.txt")
    rules, p_ratings = parse_input(in_str)
    print("Part 1:", part_1(rules, p_ratings))
    print("Part 2:", part_2(rules, p_ratings))


if __name__ == '__main__':
    main()

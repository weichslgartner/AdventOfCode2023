from collections import Counter, namedtuple
from functools import cmp_to_key
from typing import List

from aoc import get_lines


class Hand(namedtuple('Hand', 'hand hand_count bid')):
    def __repr__(self):
        return f'{self.hand} {self.hand_count} {self.bid}'


order_val = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
order_dict = {k: i for i, k in enumerate(reversed(order_val))}

order_val2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
order_dict2 = {k: i for i, k in enumerate(reversed(order_val2))}


def parse_input(lines):
    return [Hand(hand, Counter(hand), int(bid)) for hand, bid in map(str.split, lines)]


def get_highest(hand: Counter, part2=False):
    m = hand.most_common(2)
    most_com = m[0][1]
    if len(m) > 1:
        sec_com = m[1][1]
    if 'J' in hand.keys() and part2:
        for mc in hand.most_common():
            if mc[0] != 'J':
                most_com = mc[1] + hand['J']
                break
    assert most_com <= 5
    if most_com == 5:
        return 6
    if most_com == 4:
        return 5
    # full house
    if most_com == 3 and sec_com == 2:
        return 4
    if most_com == 3:
        return 3
    # two pair
    if most_com == 2 and sec_com == 2:
        return 2
    if most_com == 2:
        return 1
    return 0


def cmp_part1(c1: Hand, c2: Hand):
    return cmp(c1, c2, False)


def cmp_part2(c1: Hand, c2: Hand):
    return cmp(c1, c2, True)


def cmp(c1: Hand, c2: Hand, part2: bool):
    val_1 = get_highest(c1.hand_count, part2)
    val_2 = get_highest(c2.hand_count, part2)
    if val_1 < val_2:
        return -1
    if val_1 > val_2:
        return 1
    if part2:
        return compare_by_card_part2(c1, c2)
    return compare_by_card_part1(c1, c2)


def compare_by_card_part1(c1, c2):
    for i1, i2 in zip(c1.hand, c2.hand):
        if order_dict[i1] < order_dict[i2]:
            return -1
        if order_dict[i1] > order_dict[i2]:
            return 1
    return 0


def compare_by_card_part2(c1, c2):
    for i1, i2 in zip(c1.hand, c2.hand):
        if order_dict2[i1] < order_dict2[i2]:
            return -1
        if order_dict2[i1] > order_dict2[i2]:
            return 1
    return 0


def part_1(hand_bids: List[Hand]):
    hand_bids.sort(key=cmp_to_key(cmp_part1))
    return sum((i + 1) * h.bid for i, h in enumerate(hand_bids))


def part_2(hand_bids):
    hand_bids.sort(key=cmp_to_key(cmp_part2))
    return sum((i + 1) * h.bid for i, h in enumerate(hand_bids))


def main():
    lines = get_lines("input_07.txt")
    hand_bids = parse_input(lines)
    print("Part 1:", part_1(hand_bids))
    print("Part 2:", part_2(hand_bids))


if __name__ == '__main__':
    main()

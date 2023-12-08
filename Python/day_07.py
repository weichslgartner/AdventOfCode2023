from collections import Counter, namedtuple
from enum import IntEnum
from functools import cmp_to_key
from typing import List, Dict, Callable

from aoc import get_lines


class Hand(namedtuple('Hand', 'hand hand_count bid')):
    def __repr__(self) -> str:
        return f'{self.hand} {self.hand_count} {self.bid}'


order_val1 = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
order_dict1 = {k: i for i, k in enumerate(reversed(order_val1))}

order_val2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
order_dict2 = {k: i for i, k in enumerate(reversed(order_val2))}


class HandRank(IntEnum):
    FIVES = 6
    FOURS = 5
    FULL_HOUSE = 4
    THREES = 3
    TWO_PAIRS = 2
    PAIR = 1
    HIGHEST_CARD = 0


def parse_input(lines: List[str]) -> List[Hand]:
    return [Hand(hand, Counter(hand), int(bid)) for hand, bid in map(str.split, lines)]


def get_highest(hand: Counter, part2: bool = False) -> HandRank:
    m = hand.most_common(2)
    most_com = m[0][1]
    sec_com = m[1][1] if len(m) > 1 else 0
    if 'J' in hand.keys() and part2:
        most_com = substitute_jokers(hand, most_com)
    assert most_com <= 5
    match most_com, sec_com:
        case 5, _:
            return HandRank.FIVES
        case 4, _:
            return HandRank.FOURS
        case 3, 2:
            return HandRank.FULL_HOUSE
        case 3, _:
            return HandRank.THREES
        case 2, 2:
            return HandRank.TWO_PAIRS
        case 2, _:
            return HandRank.PAIR
        case _:
            return HandRank.HIGHEST_CARD


def substitute_jokers(hand: Hand, most_com) -> int:
    for mc in hand.most_common():
        if mc[0] != 'J':
            return mc[1] + hand['J']
    return most_com


def cmp(c1: Hand, c2: Hand, part2: bool) -> int:
    val_1 = get_highest(c1.hand_count, part2)
    val_2 = get_highest(c2.hand_count, part2)
    if val_1 != val_2:
        return 1 if val_1 > val_2 else -1
    if part2:
        return compare_by_card_part(c1, c2, order_dict2)
    return compare_by_card_part(c1, c2, order_dict1)


def compare_by_card_part(c1: Hand, c2: Hand, order_dict: Dict[str, int]) -> int:
    for i1, i2 in zip(c1.hand, c2.hand):
        if order_dict[i1] < order_dict[i2]:
            return -1
        if order_dict[i1] > order_dict[i2]:
            return 1
    return 0


def total_winnings(hand_bids: List[Hand], cmp_fun: Callable[[Hand, Hand], int]) -> int:
    hand_bids.sort(key=cmp_to_key(cmp_fun))
    return sum((i + 1) * h.bid for i, h in enumerate(hand_bids))


def part_1(hand_bids: List[Hand]) -> int:
    return total_winnings(hand_bids, lambda c1, c2: cmp(c1, c2, False))


def part_2(hand_bids: List[Hand]) -> int:
    return total_winnings(hand_bids, lambda c1, c2: cmp(c1, c2, True))


def main():
    lines = get_lines("input_07.txt")
    hand_bids = parse_input(lines)
    print("Part 1:", part_1(hand_bids))
    print("Part 2:", part_2(hand_bids))


if __name__ == '__main__':
    main()

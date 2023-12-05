import sys
from collections import namedtuple
from dataclasses import dataclass
from typing import List, Tuple

from aoc import input_as_str, extract_all_ints, chunk


class CMap(namedtuple(typename="CMap", field_names="begin end target")):
    def __repr__(self):
        return f'<{self.begin} {self.end} {self.target}>'


@dataclass
class Interval:
    begin: int
    end: int

    def __repr__(self):
        return f'-{self.begin} {self.end}-'

    def length(self):
        return self.end - self.begin + 1


def parse_input(input_str: str) -> Tuple[List[int], List[List[CMap]]]:
    all_maps = []
    seeds = None
    translation_maps = []
    for i, block in enumerate(input_str.split("\n\n")):
        for line in block.split("\n"):
            ints = extract_all_ints(line)
            if i == 0:
                seeds = ints
            elif len(ints) == 0:
                if len(translation_maps) > 0:
                    translation_maps.sort(key=lambda x: x.begin)
                    all_maps.append(translation_maps)
                translation_maps = []
                continue
            else:
                translation_maps.append(CMap(begin=ints[1], end=ints[1] + ints[2] - 1, target=ints[0]))
    translation_maps.sort(key=lambda x: x.begin)
    all_maps.append(translation_maps)
    return seeds, all_maps


def part_1(seeds: List[int], all_maps: List[List[CMap]]) -> int:
    best = sys.maxsize
    for seed in seeds:
        location = seed
        for stage in all_maps:
            location = binary_search(location, stage)
        best = min(location, best)
    return best


def convert_rages(interval: Interval, maps: List[CMap]):
    target = []
    for i, cmap in enumerate(maps):
        next_cmap = maps[i + 1] if i < len(maps) - 1 else None
        assert interval.begin <= interval.end
        # left overlap
        if cmap.end >= interval.begin >= cmap.begin:
            if cmap.end >= interval.end:
                target.append(
                    Interval(cmap.target + interval.begin - cmap.begin, cmap.target + interval.end - cmap.begin))
                return target
            else:
                target.append(Interval(cmap.target + interval.begin - cmap.begin, cmap.target + cmap.end - cmap.begin))
                interval.begin = cmap.end + 1
        # right side overlaps
        elif cmap.begin <= interval.end <= cmap.end:
            target.append(Interval(cmap.target, cmap.target + interval.end - cmap.begin))
            target.append(Interval(interval.begin, cmap.begin - 1))
            return target
        # cmap is included in interval
        elif cmap.begin >= interval.begin and cmap.end <= interval.end:
            target.append(Interval(cmap.target, cmap.target + cmap.end - cmap.begin))
            if interval.begin < cmap.begin:
                target.append(Interval(interval.begin, cmap.begin - 1))
                interval = Interval(cmap.end + 1, interval.end)
        # no overlap
        elif next_cmap is not None:
            if interval.end < next_cmap.begin:
                target.append(interval)
                return target
        else:
            target.append(interval)
            return target
    target.append(interval)
    return target if len(target) != 0 else [interval]


def binary_search(location: int, maps: List[CMap]) -> int:
    low = 0
    high = len(maps) - 1
    while low <= high:
        m = (low + high) // 2
        cmap = maps[m]
        if cmap.begin <= location <= cmap.end:
            return cmap.target + location - cmap.begin
        if cmap.end < location:
            low = m + 1
        elif cmap.begin > location:
            high = m - 1
    return location


def part_2(seeds_raw: List[int], all_maps: List[List[CMap]]) -> int:
    best = sys.maxsize
    for seed_begin, width in chunk(seeds_raw, 2):
        intervals = [Interval(seed_begin, seed_begin + width - 1)]
        for stage in all_maps:
            new_intervals = []
            for interval in intervals:
                new_intervals += convert_rages(interval, stage)
            intervals = new_intervals
        best = min(min(intervals, key=lambda x: x.begin).begin, best)
    return best


def main():
    lines = input_as_str("input_05.txt")
    seeds, all_maps = parse_input(lines)
    print("Part 1:", part_1(seeds, all_maps))
    print("Part 2:", part_2(seeds, all_maps))


if __name__ == '__main__':
    main()

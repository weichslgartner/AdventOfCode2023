import sys
from collections import namedtuple
from copy import deepcopy
from dataclasses import dataclass
from typing import List

from aoc import get_lines, input_as_str, extract_all_ints, chunk


class CMap(namedtuple(typename="CMap", field_names="begin end target")):
    def __repr__(self):
        return f'<{self.begin} {self.end} {self.target}>'


@dataclass
class Interval():
    begin: int
    end: int

    def __repr__(self):
        return f'-{self.begin} {self.end}-'


def parse_input(input):
    all_maps = []
    translation_maps = []
    seed = None
    for i, block in enumerate(input.split("\n\n")):

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


def solve(seeds, all_maps):
    best = sys.maxsize
    for seed in seeds:
        location = seed
        for stage in all_maps:
            location = binary_search(location, stage)
        # print(location)
        best = min(location, best)
       # print(location)
    return best


def part_1(seeds, all_maps):
    return solve(seeds, all_maps)


def convert(location, maps: List[CMap]):
    for cmap in maps:
        if cmap.begin <= location <= cmap.end:
            return cmap.target + location - cmap.begin
    return location


def convert2(interval: Interval, maps: List[CMap]):
    target = []
    init_interval = Interval(interval.begin,interval.end)
    # if interval.begin == 635790399:
    #     print("debug")
    n_seeds = interval.end - interval.begin
    for i, cmap in enumerate(maps):
        next_cmap = maps[i + 1] if i < len(maps) - 1 else None
        assert interval.begin <= interval.end
        # left interval overlaps or complete overlap
        if cmap.end >= interval.begin >= cmap.begin:
            if cmap.end >= interval.end:
                target.append(
                    Interval(cmap.target + interval.begin - cmap.begin, cmap.target + interval.end - cmap.begin))
                break
            else:
                target.append(Interval(cmap.target + interval.begin - cmap.begin, cmap.target + cmap.end - cmap.begin))
                interval.begin = cmap.end + 1
        # right side overlaps
        elif cmap.begin <= interval.end <= cmap.end:
            target.append(Interval(cmap.target + cmap.begin - cmap.begin, cmap.target + interval.end - cmap.begin))
            target.append(Interval(interval.begin, cmap.begin - 1))
            break

        elif cmap.begin >= interval.begin and cmap.end <= interval.end:
            target.append(Interval(cmap.target, cmap.target + cmap.end - cmap.begin))
            if interval.begin <= cmap.begin-1:
                target.append(Interval(interval.begin,cmap.begin-1))
            if cmap.end+1 <= interval.end:
                interval=Interval(cmap.end+1,interval.end)
            else:
                break
        # no overlap
        elif next_cmap is not None:
            if interval.end < next_cmap.begin:
                target.append(interval)
                break
        else:
            target.append(interval)
            break
    target.sort(key=lambda x: x.begin)
    tareget_sum = sum(i.end-i.begin for i in target)
    #if tareget_sum!=n_seeds:
       # print(tareget_sum,n_seeds,init_interval)
        #assert tareget_sum==n_seeds
    if len(target) == 0:
        #print("len(target)")
        return [interval]
    return target


def binary_search(location, maps: List[CMap]):
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


def get_all_seeds(seeds_raw):
    for begin, n in chunk(seeds_raw, 2):
        for seed in range(begin, begin + n):
            yield seed


def part_2(seeds_raw, all_maps):
    best = sys.maxsize
    for seed_begin,width in chunk(seeds_raw, 2):
        intervals = [Interval(seed_begin, seed_begin+width-1)]
        for i,stage in enumerate(all_maps):
            new_intervals = []

            for interval in intervals:
                tmp = convert2(interval,stage)
                #if tmp[0].begin == 0:
                #    print(i, tmp, interval.begin,debug_interval.begin)
                new_intervals += tmp

            #new_intervals.sort(key=lambda x: x.begin)
            #print(i,new_intervals)

            intervals = new_intervals
           # print(i, intervals)
        # print(location)
        best = min(min(intervals,key=lambda x : x.begin).begin,best)
        #print(Interval(seed_begin, seed_begin+width-1),best)
    return best


def main():
    lines = input_as_str("input_05.txt")
    seeds, all_maps = parse_input(lines)
    print("Part 1:", part_1(seeds, all_maps))
    print("Part 2:", part_2( seeds,all_maps))


if __name__ == '__main__':
    main()

import string
from collections import defaultdict
from dataclasses import dataclass
from math import prod
from typing import Any, Set, Dict

from aoc import get_lines


@dataclass
class Conjunction:
    inputs: Dict[str, bool]
    output: bool


@dataclass
class FlipFlop:
    input: bool
    state: bool


@dataclass(frozen=True)
class Pulse:
    src: str
    dst: str
    state: bool


b2l = {False: "low", True: "high"}


def parse_input(lines):
    inputs: defaultdict[Any, list] = defaultdict(list)
    outputs = defaultdict(list)
    conjunctions = set()
    flipflops = set()
    for line in lines:
        input, output = line.split("->")
        outs = [o.strip() for o in output.split(",")]
        if "%" in input:
            sym = input.strip("%" + string.whitespace)
            flipflops.add(sym)
        elif "&" in input:
            sym = input.strip("&" + string.whitespace)
            conjunctions.add(sym)
        else:
            sym = input.strip()
        for o in outs:
            inputs[o].append(sym)
            outputs[sym].append(o)
    ff_state = {f: FlipFlop(False, False) for f in flipflops}
    con_state = {c: Conjunction({i: False for i in inputs[c]}, False) for c in conjunctions}
    return inputs, outputs, con_state, ff_state


def part_1(inputs_, outputs, conj_state, ff_state):
    pulse_cnt = {False: 0, True: 0}
    for _ in range(1000):
        push_button(conj_state, ff_state, outputs, pulse_cnt)
    return prod(pulse_cnt.values())


def push_button(conj_state, ff_state, outputs, pulse_cnt):
    # push button
    pulse_cnt[False] += 1
    changed = []
    for b in outputs['broadcaster']:
        set_pulse(changed, src='broadcaster', dst=b, pulse=False, pulse_cnt=pulse_cnt)
    while len(changed) > 0:
        new_changed = []
        update_inputs(changed.copy(), conj_state)
        update_states(changed.copy(), conj_state, ff_state, new_changed, outputs, pulse_cnt)
        changed, new_changed = new_changed, []


def update_states(changed, conj_state, ff_state, new_changed, outputs, pulse_cnt):
    for c in changed:
        if c.dst in ff_state and c.state == False:
            ff_state[c.dst].state = not ff_state[c.dst].state
            for o in outputs[c.dst]:
                set_pulse(changed=new_changed, src=c.dst, dst=o, pulse=ff_state[c.dst].state, pulse_cnt=pulse_cnt)
        elif c.dst in conj_state:
            all_high = all(conj_state[c.dst].inputs.values())
            if all_high:
                conj_state[c.dst].output == False
                for o in outputs[c.dst]:
                    set_pulse(changed=new_changed, src=c.dst, dst=o, pulse=False, pulse_cnt=pulse_cnt)
            else:
                conj_state[c.dst].output == True
                for o in outputs[c.dst]:
                    set_pulse(changed=new_changed, src=c.dst, dst=o, pulse=True, pulse_cnt=pulse_cnt)


def update_inputs(changed, conj_state):
    for c in changed:
        if c.dst in conj_state:
            conj_state[c.dst].inputs[c.src] = c.state


def set_pulse(changed, src, dst, pulse, pulse_cnt):
    p = Pulse(src=src, dst=dst, state=pulse)
    pulse_cnt[pulse] += 1
    changed.append(p)


def part_2(lines):
    pass


def main():
    lines = get_lines("input_20.txt")
    inputs, outputs, conjunctions, flipflops = parse_input(lines)
    print("Part 1:", part_1(inputs, outputs, conjunctions, flipflops))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()

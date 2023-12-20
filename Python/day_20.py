import string
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from math import prod, lcm
from typing import Any, Dict, List, Tuple

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


def parse_input(lines: List[str]) -> (
        Tuple)[Dict[str, List[str]], Dict[str, List[str]], Dict[str, Conjunction], Dict[str, FlipFlop]]:
    inputs: defaultdict[Any, list] = defaultdict(list)
    outputs = defaultdict(list)
    conjunctions = set()
    flipflops = set()
    for line in lines:
        inputz, output = line.split("->")
        outs = [o.strip() for o in output.split(",")]
        if "%" in inputz:
            sym = inputz.strip("%" + string.whitespace)
            flipflops.add(sym)
        elif "&" in inputz:
            sym = inputz.strip("&" + string.whitespace)
            conjunctions.add(sym)
        else:
            sym = inputz.strip()
        for o in outs:
            inputs[o].append(sym)
            outputs[sym].append(o)
    ff_state = {f: FlipFlop(False, False) for f in flipflops}
    con_state = {c: Conjunction({i: False for i in inputs[c]}, False) for c in conjunctions}
    return inputs, outputs, con_state, ff_state


def push_button(conj_state: Dict[str, Conjunction], ff_state: Dict[str, FlipFlop], outputs: Dict[str, List[str]],
                pulse_cnt: Dict[bool, int]) -> List[Pulse]:
    # push button
    pulse_cnt[False] += 1
    all_pulses = []
    changed, new_changed = [], []
    for b in outputs['broadcaster']:
        set_pulse(changed, src='broadcaster', dst=b, pulse=False, pulse_cnt=pulse_cnt)
    while len(changed) > 0:
        update_inputs(changed, conj_state)
        update_states(changed, conj_state, ff_state, new_changed, outputs, pulse_cnt)
        changed, new_changed = new_changed, []
        all_pulses += changed
    return all_pulses


def update_states(changed: List[Pulse], conj_state: Dict[str, Conjunction], ff_state: Dict[str, FlipFlop],
                  new_changed: List[Pulse], outputs: Dict[str, List[str]], pulse_cnt: Dict[bool, int]) -> None:
    for c in changed:
        if c.dst in ff_state and c.state is False:
            ff_state[c.dst].state = not ff_state[c.dst].state
            for o in outputs[c.dst]:
                set_pulse(changed=new_changed, src=c.dst, dst=o, pulse=ff_state[c.dst].state, pulse_cnt=pulse_cnt)
        elif c.dst in conj_state:
            all_high = all(conj_state[c.dst].inputs.values())
            if all_high:
                conj_state[c.dst].output = False
                for o in outputs[c.dst]:
                    set_pulse(changed=new_changed, src=c.dst, dst=o, pulse=False, pulse_cnt=pulse_cnt)
            else:
                conj_state[c.dst].output = True
                for o in outputs[c.dst]:
                    set_pulse(changed=new_changed, src=c.dst, dst=o, pulse=True, pulse_cnt=pulse_cnt)


def update_inputs(changed: List[Pulse], conj_state: Dict[str, Conjunction]):
    for c in changed:
        if c.dst in conj_state:
            conj_state[c.dst].inputs[c.src] = c.state


def set_pulse(changed: List[Pulse], src: str, dst: str, pulse: bool, pulse_cnt: Dict[bool, int]) -> None:
    p = Pulse(src=src, dst=dst, state=pulse)
    pulse_cnt[pulse] += 1
    changed.append(p)


def part_1(outputs: Dict[str, List[str]], conj_state: Dict[str, Conjunction], ff_state: Dict[str, FlipFlop]) -> int:
    pulse_cnt = {False: 0, True: 0}
    for _ in range(1000):
        push_button(conj_state, ff_state, outputs, pulse_cnt)
    return prod(pulse_cnt.values())


def part_2(inputs: Dict[str, List[str]], outputs: Dict[str, List[str]], conj_state: Dict[str, Conjunction],
           ff_state: Dict[str, FlipFlop]) -> int:
    check_signals = inputs[inputs["rx"][0]]
    pulse_cnt = {False: 0, True: 0}
    i = 0
    cycle_high = {}
    while len(cycle_high) != len(check_signals):
        i += 1
        pulses = push_button(conj_state, ff_state, outputs, pulse_cnt)
        for p in pulses:
            if p.src in check_signals and p.state:
                cycle_high[p.src] = i
    return lcm(*cycle_high.values())


def main():
    lines = get_lines("input_20.txt")
    inputs, outputs, conj_state, ff_state = parse_input(lines)
    print("Part 1:", part_1(outputs, deepcopy(conj_state), deepcopy(ff_state)))
    print("Part 2:", part_2(inputs, outputs, conj_state, ff_state))


if __name__ == '__main__':
    main()

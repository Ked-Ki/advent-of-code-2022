from itertools import islice, tee
from collections import Counter


def run(ls, mark_len):
    it_l, it_r = tee(iter(ls))
    chr_set = Counter(islice(it_r, mark_len))
    r_idx = mark_len
    while len(chr_set.keys()) < mark_len:
        rm_elem = next(it_l)
        chr_set[rm_elem] -= 1
        if chr_set[rm_elem] == 0:
            del chr_set[rm_elem]
        new_elem = next(it_r)
        chr_set[new_elem] += 1
        r_idx += 1
    return r_idx


def part1(ls):
    return run(next(ls), 4)


def part2(ls):
    return run(next(ls), 14)

import util.logging as log
from itertools import islice
from functools import reduce


def split_l(s):
    mid = (len(s) + 1) // 2
    return (s[:mid], s[mid:])


def chr_to_int(c):
    if c.islower():
        return ord(c) - ord("a") + 1
    else:
        return ord(c) - ord("A") + 1 + 26


def part1(ls):
    total = 0
    for c1, c2 in map(split_l, ls):
        shared = set(c1) & set(c2)
        item = shared.pop()
        priority = chr_to_int(item)
        log.p1_log.debug(f"{c1=} {c2=} {item=} {priority=}")
        total += priority
    return total


def part2(ls):
    total = 0
    while group := list(islice(ls, 3)):
        shared = reduce(set.intersection, map(set, group))
        item = shared.pop()
        total += chr_to_int(item)
    return total

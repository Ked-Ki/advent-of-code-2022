import bisect
from itertools import takewhile

def run(elves, num=1):
    top = [-1] * num
    while (elf := list(takewhile( lambda l: l != "", elves))):
        bisect.insort(top, sum(map(int, elf)))
        top = top[-num:]
    return top


def part1(ls):
    return sum(run(ls))


def part2(ls):
    return sum(run(ls, num=3))

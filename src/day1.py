from itertools import takewhile
from util.moreiters import top_n


def run(elves, num=1):
    def sum_it():
        while (elf := list(takewhile(lambda s: s != "", elves))):
            yield sum(map(int, elf))

    return top_n(sum_it(), num)


def part1(ls):
    return sum(run(ls))


def part2(ls):
    return sum(run(ls, num=3))

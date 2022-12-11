import logging

import itertools

parse_log = logging.getLogger("parse")

def parse(ls):
    crates_strs = list(itertools.takewhile(lambda l: l != "", ls))
    parse_log.debug(f'{crates_strs=}')
    crates = parse_crates(crates_strs)

    moves_strs = ls 
    parse_log.debug(f'{moves_strs=}')
    moves = map(parse_move, moves_strs)

    return (crates, moves)


def parse_crates(ls):
    num_crates = len(ls[-1].split())
    rows = iter(ls[-2::-1])

    def parse_row(r):
        it = iter(r)
        while (c := list(itertools.islice(it, 4))):
            yield ''.join(c).rstrip().strip("[]")

    p_rows = list(map(lambda r: list(parse_row(r)), rows))
    parse_log.debug(f'{p_rows=}')

    stacks = [[r for row in p_rows if (r := row[i])] for i in range(num_crates)]
    parse_log.debug(f'{stacks=}')

    return stacks


class Move:
    def __init__(self, count, from_s, to_s):
        self.count = count
        self.from_s = from_s
        self.to_s = to_s

    def do_move1(self, crates):
        for _ in range(self.count):
            c = crates[self.from_s].pop()
            crates[self.to_s].append(c)

    def do_move2(self, crates):
        cs = crates[self.from_s][-self.count:]
        del crates[self.from_s][-self.count:]
        crates[self.to_s] += cs


def parse_move(l):
    words = l.split()
    cnt, from_s, to_s = int(words[1]), int(words[3]), int(words[5])
    return Move(cnt, from_s-1, to_s-1)


def part1(ls):
    cs, mvs = parse(ls)

    logging.debug(f'{cs=}, {mvs=}')

    for mv in mvs:
        mv.do_move1(cs)
        logging.debug(f"{cs=}")

    return ''.join([c[-1] for c in cs])


def part2(ls):
    cs, mvs = parse(ls)

    for mv in mvs:
        mv.do_move2(cs)
        logging.debug(f"{cs=}")

    return ''.join([c[-1] for c in cs])

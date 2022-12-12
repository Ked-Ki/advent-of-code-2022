def parse_l(s):
    rs = s.split(",")
    return map(lambda r: tuple(map(int, r.split("-"))), rs)


def point_in(p, r):
    return r[0] <= p and p <= r[1]


def included(r1, r2):
    return all(map(lambda p: point_in(p, r2), r1)) or all(
        map(lambda p: point_in(p, r1), r2)
    )


def part1(ls):
    return sum(1 for rs in map(parse_l, ls) if included(*rs))


def overlap(r1, r2):
    return any(map(lambda p: point_in(p, r2), r1)) or any(
        map(lambda p: point_in(p, r1), r2)
    )


def part2(ls):
    return sum(1 for rs in map(parse_l, ls) if overlap(*rs))

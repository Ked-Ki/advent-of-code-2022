import util.logging as log
import re
import bisect
import itertools as it


def parse_line(line):
    int_re = "(-?[0-9]*)"
    match = re.match(
        f"Sensor at x={int_re}, y={int_re}: "
        + f"closest beacon is at x={int_re}, y={int_re}",
        line,
    )
    return ((int(match[1]), int(match[2])), (int(match[3]), int(match[4])))


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class RangeSet:
    def __init__(self):
        # sorted list of all range endpoints
        self.arr = []

    def insert(self, rng):
        # endpoints are logically grouped like so
        # ---[a1, b1]---[a2, b2]---[a3, b3]---

        # find each endpoint
        # use bisect_left for left bound in case it equals an existing right bound. bisect_left
        # returns the leftmost index for equal elements, meaning our indexes do overlap.
        # & sim for right
        l_index = bisect.bisect_left(self.arr, rng[0])
        r_index = bisect.bisect_right(self.arr, rng[1])

        # exploit the fact that right/left bounds are odd/even
        l_in_range = l_index % 2 != 0
        r_in_range = r_index % 2 != 0
        if not l_in_range and not r_in_range:
            # l and r both between ranges
            # ---[a1, b1]---[a2, b2]---[a3, b3]---
            #  l          r
            # they should subsume everything inside
            self.arr[l_index:r_index] = rng
        elif not l_in_range and r_in_range:
            # l between ranges, r not
            # ---[a1, b1]---[a2, b2]---[a3, b3]---
            #  l                r
            # extend range left
            self.arr[l_index:r_index] = (rng[0],)
        elif l_in_range and not r_in_range:
            # l in range, r not
            # ---[a1, b1]---[a2, b2]---[a3, b3]---
            #       l                r
            # extend range right
            self.arr[l_index:r_index] = (rng[1],)
        elif l_in_range and r_in_range:
            # both in different ranges
            # ---[a1, b1]---[a2, b2]---[a3, b3]---
            #       l           r
            # delete all endpoints between them
            self.arr[l_index:r_index] = []

    def size(self):
        return sum(r - l + 1 for l, r in self)

    def __iter__(self):
        arr_iter = iter(self.arr)
        while rng := tuple(it.islice(arr_iter, 2)):
            yield rng

    def __repr__(self):
        return f"RangeSet(arr={self.arr})"


def part1(strs, report_row, **_kw_args):
    blocked_set = RangeSet()
    beacon_set = set()
    for s, b in map(parse_line, strs):
        if b[1] == report_row:
            beacon_set.add(b[0])
        d = dist(s, b)
        v_d = abs(s[1] - report_row)
        l = s[0] - (d - v_d)
        r = s[0] + (d - v_d)
        if l <= r:
            log.p1_log.debug(f"{s=} {b=} {d=} {v_d=} {l=} {r=}")
            blocked_set.insert((l, r))
        else:
            log.p1_log.debug(f"range empty{s=} {b=} {d=} {v_d=}")
        log.p1_log.debug(f"{blocked_set=} {beacon_set=}")
    return blocked_set.size() - len(beacon_set)


def part2(strs, search_bound, **_kw_args):
    sb_list = list(map(parse_line, strs))
    for y in range(search_bound + 1):
        log.p2_log.debug(f"searching row {y}")
        blocked_set = RangeSet()
        for s, b in sb_list:
            d = dist(s, b)
            v_d = abs(s[1] - y)
            l = max(0, s[0] - (d - v_d))
            r = min(search_bound, s[0] + (d - v_d))
            if l <= r:
                new_range = (l, r)
                log.p1_log.debug(f"{s=} {b=} {d=} {v_d=} {l=} {r=}")
                blocked_set.insert((l, r))
            else:
                log.p2_log.debug(f"range empty{s=} {b=} {d=} {v_d=}")
            log.p2_log.debug(f"{blocked_set=}")
        rng = next(iter(blocked_set))
        log.p2_log.debug(f"searched row {y}, first range={rng}")
        if rng != (0, search_bound):
            # found a gap!
            x = rng[1] + 1
            return x * 4000000 + y

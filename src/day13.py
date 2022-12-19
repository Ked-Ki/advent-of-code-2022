import itertools as it
import functools as ft
import util.logging as log
import bisect


def parse_list(p):
    # remove outermost brackets
    trim_p = p[1:-1]

    nest_count = 0
    cur_str = ""
    for c in trim_p:
        if c == "," and nest_count == 0:
            out_str = cur_str
            cur_str = ""
            yield out_str
        else:
            if c == "]":
                nest_count -= 1
            elif c == "[":
                nest_count += 1
            cur_str += c

    if cur_str != "":
        yield cur_str


def compare_pair(p1, p2):
    log.p1_log.debug(f"comparing {p1=} {p2=}")
    p1_list = p1[0] == "["
    p2_list = p2[0] == "["

    if p1_list and p2_list:
        log.p1_log.debug("two lists")
        for new_p1, new_p2 in it.zip_longest(parse_list(p1), parse_list(p2)):
            if new_p1 is None and new_p2 is not None:
                log.p1_log.debug("p1 empty; p1 < p2 --> -1")
                return -1
            elif new_p1 is not None and new_p2 is None:
                log.p1_log.debug("p2 empty; p1 > p2 --> 1")
                return 1
            else:
                cmp = compare_pair(new_p1, new_p2)
                if cmp != 0:
                    return cmp
                else:
                    continue
        log.p1_log.debug("end of both lists; p1 == p2 --> 0")
        return 0
    elif not p1_list and not p2_list:
        # ints, just compare
        log.p1_log.debug(f"two ints {p1=} {p2=} ")
        return int(p1) - int(p2)
    elif not p1_list:
        log.p1_log.debug("p1 int; p2 list")
        # p1 is not list, p2 is
        return compare_pair(f"[{p1}]", p2)
    elif not p2_list:
        log.p1_log.debug("p1 list; p2 int")
        # p1 is list, p2 is not
        return compare_pair(p1, f"[{p2}]")


def part1(strs, **_kw_args):
    pair_idx = 0
    correct_order = []
    while pair := list(it.takewhile(lambda s: s != "", strs)):
        pair_idx += 1
        log.p1_log.debug(f"running pair #{pair_idx} {pair}")
        cmp = compare_pair(*pair)
        log.p1_log.debug(f"pair #{pair_idx}: {cmp=}")
        if cmp <= 0:
            correct_order.append(pair_idx)
    log.p1_log.debug(f"{correct_order=}")
    return sum(correct_order)


def part2(strs, **_kw_args):
    div1 = "[[2]]"
    div2 = "[[6]]"

    all_packets = it.chain((div1, div2), filter(lambda s: s != "", strs))
    key_f = ft.cmp_to_key(compare_pair)
    sorted_packets = sorted(all_packets, key=key_f)
    log.p2_log.debug(f"{sorted_packets=}")

    div1_i = bisect.bisect_right(sorted_packets, key_f(div1), key=key_f)
    div2_i = bisect.bisect_right(sorted_packets, key_f(div2), key=key_f)
    log.p2_log.debug(f"{div1_i=}, f{div2_i=}")
    return div1_i * div2_i

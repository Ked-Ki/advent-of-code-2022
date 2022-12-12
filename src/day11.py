import itertools as itool
import util.moreiters as moreiters
import collections as c
import util.morecollections as morec
import util.logging as log
from util.morefuncs import ReprFunc
import math


class Monkey:
    def __init__(self, num, items, op, test, reduce_worry):
        self.num = num
        self.items = items
        self.op = op
        self.test = test
        self.inspect_count = 0
        self.reduce_worry = reduce_worry

    def __repr__(self):
        return (
            f"Monkey({self.num=},{self.items=},{self.op=},"
            + f"{self.test=},{self.inspect_count=},{self.reduce_worry=})"
        )

    def throw_all(self):
        for item in morec.consume_deque(self.items, from_left=True):
            new_item = self.reduce_worry(self.op(item))
            self.inspect_count += 1
            yield (self.test(new_item), new_item)

    def catch(self, item):
        self.items.append(item)


class TestFunc(ReprFunc):
    def __init__(self, modulus, true_num, false_num):
        super().__init__(
            lambda v: true_num if v % modulus == 0 else false_num,
            f"({modulus} | v ? {true_num} : {false_num})",
        )
        self.modulus = modulus


def parse_op(s):
    expr = s.split()[3:]
    v1, op, v2 = expr

    def op_func(o):
        nonlocal expr
        nonlocal v1, op, v2

        def parse_val(v):
            nonlocal o
            if v == "old":
                return o
            else:
                return int(v)

        pv1, pv2 = parse_val(v1), parse_val(v2)

        if op == "*":
            return pv1 * pv2
        elif op == "+":
            return pv1 + pv2

    return ReprFunc(op_func, f"({v1} {op} {v2})")


def parse_test(test_strs):
    modulus = int(test_strs[0].split()[3])
    true_num = int(test_strs[1].split()[5])
    false_num = int(test_strs[2].split()[5])

    return TestFunc(modulus, true_num, false_num)


def parse(ls, reduce_worry):
    monkeys = []
    while monk_str := list(itool.takewhile(lambda s: s != "", ls)):
        m_args = {}
        m_args["num"] = int(monk_str[0].rstrip(":").split()[1])
        m_args["items"] = c.deque(
            map(lambda s: int(s.rstrip(",")), monk_str[1].split()[2:])
        )
        m_args["op"] = parse_op(monk_str[2])
        m_args["test"] = parse_test(monk_str[3:])
        m_args["reduce_worry"] = reduce_worry

        m = Monkey(**m_args)
        log.parse_log.debug(f"{m}")
        monkeys.append(m)
    return monkeys


def simulate(monkeys, num_rounds):
    for round_n in range(num_rounds):
        for monkey in monkeys:
            for new_m, item in monkey.throw_all():
                monkeys[new_m].catch(item)
                log.p1_log.debug(f"threw {item} to {new_m}; {monkey=}")

        log.p1_log.debug(f"round {round_n} end: {monkeys=}")


def part1(ls):
    monkeys = parse(ls, ReprFunc(lambda w: w // 3, "(w//3)"))
    simulate(monkeys, 20)
    m1, m2 = moreiters.top_n((m.inspect_count for m in monkeys), 2)
    return m1 * m2


def part2(ls):
    monkeys = parse(ls, None)

    # in this part the worry levels get very large, reduce mod lcm
    # using lcm of all moduli preserves divisibility tests
    reduction_mod = math.lcm(*(m.test.modulus for m in monkeys))
    for m in monkeys:
        m.reduce_worry = ReprFunc(lambda w: w % reduction_mod, f"(w%{reduction_mod})")

    simulate(monkeys, 10000)
    m1, m2 = moreiters.top_n((m.inspect_count for m in monkeys), 2)
    return m1 * m2

import util.logging as log
from math import copysign
from itertools import pairwise


class State:
    def __init__(self, length=2):
        self.length = length
        self.knots = [(0, 0)] * self.length

    def get_tail(self):
        return self.knots[-1]

    def update_head(self, dx, dy):
        self.knots[0] = (self.knots[0][0] + dx, self.knots[0][1] + dy)
        log.run_log.debug(f"updated head: {self=}")

    def update_tail(self):
        for idx1, idx2 in pairwise(range(self.length)):
            self.move_towards(idx1, idx2)

    def move_towards(self, idx1, idx2):
        dx = self.knots[idx1][0] - self.knots[idx2][0]
        dy = self.knots[idx1][1] - self.knots[idx2][1]
        if abs(dx) > 1 or abs(dy) > 1:
            ddx = int(copysign(1, dx)) if dx else 0
            ddy = int(copysign(1, dy)) if dy else 0
            log.run_log.debug(f"updating tail: {dx=}, {ddx=}, {dy=}, {ddy=}")
            self.knots[idx2] = (self.knots[idx2][0] + ddx, self.knots[idx2][1] + ddy)
        log.run_log.debug(f"updated tail: {self=}")

    def __repr__(self):
        return f"state({self.knots=})"


def run(length, ls):
    vis = set()
    st = State(length=length)
    vis.add(st.get_tail())
    for s in ls:
        ws = s.split()
        for _ in range(int(ws[1])):
            if ws[0] == "R":
                st.update_head(1, 0)
            elif ws[0] == "L":
                st.update_head(-1, 0)
            elif ws[0] == "U":
                st.update_head(0, 1)
            elif ws[0] == "D":
                st.update_head(0, -1)
            st.update_tail()
            vis.add(st.get_tail())
        log.run_log.debug(f"{st=}")

    return len(vis)


def part1(ls):
    return run(2, ls)


def part2(ls):
    return run(10, ls)

import util.logging as log
import functools
import itertools as itool
from util.moreiters import takewhile_inclusive
from util.grid import Grid


def part1(ls):
    grid = Grid([[int(t) for t in row] for row in ls])
    blocks = {d: Grid.filled(grid.w, grid.h, default=0)
              for d in ["L", "D", "U", "R"]}

    LU_vis = set()
    RD_vis = set()

    for i in range(grid.h):
        for j in range(grid.w):
            t = grid.get(i, j)
            l_blk = blocks["L"].get(i, j - 1, default=-1)
            u_blk = blocks["U"].get(i - 1, j, default=-1)
            if l_blk < t or u_blk < t:
                LU_vis.add((i, j))
            blocks["L"].set(i, j, max(l_blk, t))
            blocks["U"].set(i, j, max(u_blk, t))

    for i in range(grid.h - 1, -1, -1):
        for j in range(grid.w - 1, -1, -1):
            t = grid.get(i, j)
            r_blk = blocks["R"].get(i, j + 1, default=-1)
            d_blk = blocks["D"].get(i + 1, j, default=-1)
            if r_blk < t or d_blk < t:
                RD_vis.add((i, j))
            blocks["R"].set(i, j, max(r_blk, t))
            blocks["D"].set(i, j, max(d_blk, t))

    return len(LU_vis | RD_vis)


def part2(ls):
    grid = Grid([[int(t) for t in row] for row in ls])

    max_score = 0

    for i in range(grid.h):
        for j in range(grid.w):
            t = grid.get(i, j)

            l_ts = (grid.get(i, j - d) for d in itool.count(1))
            r_ts = (grid.get(i, j + d) for d in itool.count(1))
            u_ts = (grid.get(i - d, j) for d in itool.count(1))
            d_ts = (grid.get(i + d, j) for d in itool.count(1))

            def filter_visible(ts):
                exists = itool.takewhile(lambda s: s is not None, ts)
                return takewhile_inclusive(lambda s: s < t, exists)

            dir_scores = [sum(1 for s in filter_visible(ts))
                          for ts in [l_ts, r_ts, u_ts, d_ts]]

            log.p2_log.debug(f"{dir_scores=}")

            score = functools.reduce(lambda a, b: a * b, dir_scores)

            log.p2_log.debug(f"({i},{j}) {t=} {score=}")

            max_score = max(score, max_score)

    return max_score

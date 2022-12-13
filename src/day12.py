from util.grid import Grid, Dir
import collections
import util.logging as log
import functools as ft


def find_grid(g, c):
    found = None
    for idx, d in g.enumerate_iter():
        log.parse_log.debug(f"{idx=}, {d=}")
        if d == c:
            found = idx
            break
    return found


def part1(strs):
    grid = Grid.from_str(strs)

    start_idx = find_grid(grid, "S")
    end_idx = find_grid(grid, "E")

    grid.set(*start_idx, "a")
    grid.set(*end_idx, "z")

    log.parse_log.debug(f"{start_idx=}, {end_idx=}")

    # two bfs's, forward (S to E) (_f) and backwards (E to S) (_b)
    to_visit_f = collections.deque([(start_idx, 0)])
    visited_f = Grid.filled(grid.w, grid.h)
    visited_f.set(*start_idx, 0)

    to_visit_b = collections.deque([(end_idx, 0)])
    visited_b = Grid.filled(grid.w, grid.h)
    visited_b.set(*end_idx, 0)

    def find_new_neighbors(i, j, is_reachable, visit_grid):
        for d in Dir:
            idx = d.add(i, j)
            v = grid.get(*idx)
            v_g = visit_grid.get(*idx)

            if v is not None and v_g is None and is_reachable(v):
                log.p1_log.debug(f"found neighbor old_idx={(i,j)} {idx=} {v=}")
                yield idx

    f_reach = lambda cur, nxt: nxt <= chr(ord(cur) + 1)
    b_reach = lambda cur, nxt: cur <= chr(ord(nxt) + 1)

    def visit_next(to_visit, visited, is_reachable_from, direction):
        while True:
            idx, p_len = to_visit.pop()
            if visited.get(*idx):
                log.p1_log.debug(f"visited {direction} {idx=} twice, skipping")
                continue

            cur_v = grid.get(*idx)

            log.p1_log.debug(f"visit {direction} {idx=} {p_len=}, {cur_v=}")

            visited.set(*idx, p_len)
            for n in find_new_neighbors(
                *idx, ft.partial(is_reachable_from, cur_v), visited
            ):
                to_visit.appendleft((n, p_len + 1))
            return (idx, p_len)

    def pprint_visited(visited):
        def v_to_chr(v):
            if v is None:
                return " " * 3
            else:
                return f"{v:3d}"

        return visited.pprint(h_join=",", v_to_chr=v_to_chr)

    while to_visit_f or to_visit_b:
        log.p1_log.debug(f"loop forward start: {to_visit_f=}")
        f_idx, f_p_len = visit_next(to_visit_f, visited_f, f_reach, "forward")
        if known_b := visited_b.get(*f_idx):
            log.p1_log.debug(f"met forwards at {f_idx}, {f_p_len=}, {known_b=}")
            return f_p_len + known_b
        log.p1_log.debug(f"loop forward end: {to_visit_f=}")
        log.p1_log.debug(f"visited_f:\n{pprint_visited(visited_f)}")

        log.p1_log.debug(f"loop backward start: {to_visit_b=}")
        b_idx, b_p_len = visit_next(to_visit_b, visited_b, b_reach, "backward")
        if known_f := visited_f.get(*b_idx):
            log.p1_log.debug(f"met backwards at {b_idx}, {b_p_len=}, {known_f=}")
            return b_p_len + known_f
        log.p1_log.debug(f"loop backward end: {to_visit_b=}")
        log.p1_log.debug(f"visited_b:\n{pprint_visited(visited_b)}")


def part2(strs):
    pass

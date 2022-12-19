import itertools as it
import util.grid as g
import util.logging as log


def parse(strs):
    scan_grid = g.Grid([["+"]], index_args=(g.XD_INDEX | g.ZERO(500, 0)))
    for path in strs:
        for line in it.pairwise(path.split(" -> ")):
            start_p = tuple(map(int, line[0].split(",")))
            end_p = tuple(map(int, line[1].split(",")))
            d = g.dir_to(*start_p, *end_p, index=g.XD_INDEX)
            if d == None:
                log.parse_log.error("error: line endpoints equal")
                raise Exception()
            cur_p = start_p
            while cur_p != end_p:
                scan_grid.set(*cur_p, "#", default=".", resize=True)
                cur_p = g.add_dir(d, *cur_p, index=g.XD_INDEX)
            scan_grid.set(*end_p, "#", default=".", resize=True)

    log.parse_log.debug(f"parsed input, grid:\n{scan_grid}")
    return scan_grid


def part1(strs):
    scan_grid = parse(strs)

    BLOCKED = "blocked"
    ABYSS = "abyss"

    def sand_step(cur_s):
        down_s = g.add_dir(g.Dir.D, *cur_s, index=g.XD_INDEX)
        downleft_s = g.add_dir(g.Dir.L, *down_s, index=g.XD_INDEX)
        downright_s = g.add_dir(g.Dir.R, *down_s, index=g.XD_INDEX)

        cand_ps = [down_s, downleft_s, downright_s]
        gets = map(lambda p: (p, scan_grid.get(*p, default=ABYSS)), cand_ps)

        for new_p, result in gets:
            if result == ABYSS:
                return ABYSS
            elif result == ".":
                return new_p

        return BLOCKED

    def sim_sand_unit():
        cur_s = (500, 0)
        while True:
            new_s = sand_step(cur_s)
            if new_s == BLOCKED:
                scan_grid.set(*cur_s, "o")
                return BLOCKED
            elif new_s == ABYSS:
                return ABYSS
            else:
                cur_s = new_s

    num_sands = 0
    while (sand_result := sim_sand_unit()) != ABYSS:
        num_sands += 1
        log.p1_log.debug(f"sim {num_sands=}, grid:\n{scan_grid}")

    return num_sands


def part2(strs):
    scan_grid = parse(strs)

    (l_bound, _), (r_bound, max_depth) = scan_grid.bounds()

    max_depth += 2
    for x in range(l_bound, r_bound + 1):
        scan_grid.set(x, max_depth, "#", default=".", resize=True)

    log.p2_log.debug(f"added initial floor, grid=\n{scan_grid}")

    BLOCKED = "blocked"
    STOPPED = "stopped"

    def sand_step(cur_s):
        down_s = g.add_dir(g.Dir.D, *cur_s, index=g.XD_INDEX)
        downleft_s = g.add_dir(g.Dir.L, *down_s, index=g.XD_INDEX)
        downright_s = g.add_dir(g.Dir.R, *down_s, index=g.XD_INDEX)

        if down_s[1] == max_depth:
            # hit floor, extend if needed
            scan_grid.set(*down_s, "#", default=".", resize=True)
            return BLOCKED

        cand_ps = [down_s, downleft_s, downright_s]
        gets = map(lambda p: (p, scan_grid.get(*p, default=".", resize=True)), cand_ps)

        for new_p, result in gets:
            if result == ".":
                return new_p

        return BLOCKED

    def sim_sand_unit():
        source = (500, 0)
        cur_s = source
        while True:
            new_s = sand_step(cur_s)
            if new_s == BLOCKED:
                if cur_s == source:
                    return STOPPED
                else:
                    scan_grid.set(*cur_s, "o")
                    return BLOCKED
            else:
                cur_s = new_s

    num_sands = 0
    while (sand_result := sim_sand_unit()) != STOPPED:
        num_sands += 1
        log.p2_log.debug(f"sim {num_sands=}, grid:\n{scan_grid}")

    # add one for sand that stopped the spout
    return num_sands + 1

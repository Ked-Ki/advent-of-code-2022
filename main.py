#! /usr/bin/env python3

import argparse
import logging
import os.path
import importlib
import sys
import itertools
import glob


def parser():
    parser = argparse.ArgumentParser(description=f"run day")
    parser.add_argument("day_num", nargs="?", default="all", 
                        help="day to run. if absent, run all days")
    parser.add_argument("-s", "--sample", action="store_true",
                        help="use sample input")
    parser.add_argument("-d", "--debug", nargs="*", help="print logs")

    return parser


def logging_config(debug_arg):
    handler = logging.StreamHandler()
    if debug_arg is not None:
        if debug_arg != []:
            handler.addFilter(lambda r: r.name in debug_arg)
        level = logging.DEBUG
    else:
        level = logging.WARNING
    logging.basicConfig(handlers=[handler], level=level)


class DayNotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"DayNotFoundError: {self.msg}"


def import_day(day_num):
    mod_name = f"day{day_num}"
    path = f"src/{mod_name}.py"
    if os.path.exists(path):
        return importlib.import_module(f"src.{mod_name}")
    else:
        raise DayNotFoundError(f"couldn't find {path}")


def get_input(day_num, use_sample):
    dir_name = None
    if use_sample:
        dir_name = f"samples/day{day_num}"
    else:
        dir_name = f"inputs/day{day_num}"

    found_input = False
    
    for in_path in glob.iglob(os.path.join(dir_name, "in*")):
        found_input = True
        in_tag = os.path.basename(in_path).removeprefix("in")

        # read answers if present
        part1_ans = part2_ans = None
        out_file = os.path.join(dir_name, f"out{in_tag}")
        if os.path.exists(out_file):
            with open(out_file) as f:
                answers = list(map(lambda l: l.rstrip("\n"), f.readlines()))
                part1_ans = answers[0] if answers[0] != "None" else None
                part2_ans = answers[1] if answers[1] != "None" else None

        yield (in_path, part1_ans, part2_ans)

    if not found_input:
        raise DayNotFoundError(f"couldn't find any inputs in {dir_name}")


tty_blu = "\x1b[34m"
tty_grn = "\x1b[32m"
tty_red = "\x1b[31m"
tty_yel = "\x1b[33m"
tty_rst = "\x1b[0m"

def colorize(s, color):
    istty = sys.stdout.isatty()
    if istty:
        return f"{color}{s}{tty_rst}"
    else:
        return s


def get_status(result, ans):
    if ans is None:
        return colorize("(????)", tty_yel)
    elif str(result) == ans:
        return colorize("(PASS)", tty_grn)
    else:
        return colorize(f"(FAIL) {ans}", tty_red)


if __name__ == "__main__":
    args = parser().parse_args()
    logging_config(args.debug)
    if args.day_num != "all":
        days = [args.day_num]
    else:
        days = map(str, range(1, 26))

    for day_num in days:
        try: 
            day = import_day(day_num)
        except DayNotFoundError as err:
            if args.day_num != "all":
                print(err)
                sys.exit(1)
            else:
                continue
        print(f"{colorize('day:',tty_blu)} {day_num}")

        try:
            for in_path, part1_ans, part2_ans in get_input(day_num, args.sample):
                with open(in_path) as f:
                    print(f"{colorize('input:',tty_blu)} {in_path}")
                    part1_in, part2_in = itertools.tee(map(lambda l: l.rstrip("\n"), 
                                                           f.readlines()))
                    part1_res = day.part1(part1_in)
                    part1_stat = get_status(part1_res, part1_ans)
                    print(f"{colorize('part 1:',tty_blu)} {part1_res} {part1_stat}")
                    part2_res = day.part2(part2_in)
                    part2_stat = get_status(part2_res, part2_ans)
                    print(f"{colorize('part 2:',tty_blu)} {part2_res} {part2_stat}")
        except DayNotFoundError as err:
            print(err)
            sys.exit(1)

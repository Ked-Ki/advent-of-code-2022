import logging

# logs specific to one part
p1_log = logging.getLogger("part1")
p2_log = logging.getLogger("part2")

# logs shared by both parts
run_log = logging.getLogger("run")

# logs during parsing
parse_log = logging.getLogger("parse")

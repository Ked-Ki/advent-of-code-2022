from util.grid import Grid


class State:
    def __init__(self, x=1, cycle=1, tick_hook=None):
        self.x = x
        self.cycle = cycle
        if tick_hook:
            self.tick_hook = tick_hook
        else:
            self.tick_hook = lambda st: ()

    def tick(self):
        self.tick_hook(self)
        self.cycle += 1

    def run_noop(self):
        self.tick()

    def run_addx(self, n):
        self.tick()
        self.tick()
        self.x += n

    def run_instr(self, s):
        if s.startswith("noop"):
            self.run_noop()
        elif s.startswith("addx"):
            _, i = s.split()
            self.run_addx(int(i))


def part1(ls):
    out = 0

    def tick_hook(st):
        nonlocal out
        if (st.cycle % 40 == 20):
            cur_strength = st.cycle * st.x
            out += cur_strength

    state = State(tick_hook=tick_hook)

    for s in ls:
        state.run_instr(s)

    return out


def part2(ls):
    crt = Grid.filled(40, 6, default=".")

    pixel = 0
    row = 0

    def tick_hook(st):
        nonlocal pixel, row
        if abs(st.x - pixel) <= 1:
            crt.set(row, pixel, "#")
        pixel += 1
        if pixel >= 40:
            row += 1
            pixel = 0
        if row >= 6:
            row = 0

    state = State(tick_hook=tick_hook)

    for s in ls:
        state.run_instr(s)

    result = str(crt)

    return f"\n{result}"

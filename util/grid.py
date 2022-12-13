from enum import Enum, auto


class Dir(Enum):
    L = auto()
    R = auto()
    U = auto()
    D = auto()

    def add(self, i, j, n=1):
        if self == Dir.L:
            return (i, j - n)
        elif self == Dir.R:
            return (i, j + n)
        elif self == Dir.U:
            return (i - n, j)
        elif self == Dir.D:
            return (i + n, j)


class Grid:
    def __init__(self, arr):
        self.arr = arr
        self.w = len(arr[0])
        self.h = len(arr)

    def inbounds(self, i, j):
        return i >= 0 and i < self.h and j >= 0 and j < self.w

    def get(self, i, j, default=None):
        if self.inbounds(i, j):
            return self.arr[i][j]
        else:
            return default

    def set(self, i, j, x):
        self.update(i, j, lambda _: x)

    def update(self, i, j, f):
        if self.inbounds(i, j):
            c = self.arr[i][j]
            self.arr[i][j] = f(c)

    @staticmethod
    def filled(w, h, default=None):
        return Grid([[default] * w for _ in range(h)])

    @staticmethod
    def from_str(s, chr_to_v=lambda c: c):
        lines = None
        if isinstance(s, str):
            lines = s.split("\n")
        else:
            # assuming this is an iter of strs, one per row
            lines = s

        return Grid([[chr_to_v(c) for c in row] for row in lines])

    def enumerate_iter(self):
        return (((i, j), self.get(i, j)) for i in range(self.h) for j in range(self.w))

    def __iter__(self):
        return (self.get(i, j) for i in range(self.h) for j in range(self.w))

    def __repr__(self):
        return f"Grid(w={self.w},h={self.h},arr={self.arr})"

    def __str__(self):
        return self.pprint()

    def pprint(self, h_join="", v_join="\n", v_to_chr=str):
        return v_join.join(map(h_join.join, map(lambda r: map(v_to_chr, r), self.arr)))

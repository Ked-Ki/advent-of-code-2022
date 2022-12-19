from enum import Enum, auto
import itertools as it


class Dir(Enum):
    L = auto()
    R = auto()
    U = auto()
    D = auto()

    def ortho(self, d):
        if self.is_h() and d.is_v():
            return True
        elif self.is_v() and d.is_h():
            return True
        else:
            return False

    def is_v(self):
        return self == Dir.U or self == Dir.D

    def is_h(self):
        return self == Dir.L or self == Dir.R


class Index:
    def __init__(self, h, w, c1_dir=Dir.D, c2_dir=Dir.R, z1=0, z2=0):
        self.h = h
        self.w = w
        if not c1_dir.ortho(c2_dir):
            raise Exception(f"Invalid axes directions {c1_dir} {c2_dir}")
        self.c1_dir = c1_dir
        self.c2_dir = c2_dir
        self._flip = c1_dir.is_h()
        self._h_neg = Index._dir_is_neg(c1_dir if self._flip else c2_dir)
        self._v_neg = Index._dir_is_neg(c2_dir if self._flip else c1_dir)
        self.z1 = z1
        self.z2 = z2

    @staticmethod
    def _dir_is_neg(d):
        return d == Dir.L or d == Dir.U

    def _neg_if_v(self, c):
        return self.h - c - 1 if self._v_neg else c

    def _neg_if_h(self, c):
        return self.w - c - 1 if self._h_neg else c

    def _flip_if(self, *c):
        if self._flip:
            return c[::-1]
        else:
            return c

    def g_coord(self, c1, c2):
        i, j = self._flip_if(c1 - self.z1, c2 - self.z2)
        return (self._neg_if_v(i), self._neg_if_h(j))

    def u_coord(self, i, j):
        c1_adj, c2_adj = self._flip_if(self._neg_if_v(i), self._neg_if_h(j))
        return (c1_adj + self.z1, c2_adj + self.z2)

    def resize(self, c1, c2):
        u_v, u_h = self._flip_if(c1 - self.z1, c2 - self.z2)
        if u_h > 0:
            w_r = {"needed": u_h + 1 - self.w, "new": u_h + 1, "prepend": self._h_neg}
        else:
            w_r = {"needed": -u_h, "new": self.w - u_h, "prepend": not self._h_neg}
            if self._flip:
                self.z1 = self.z1 + u_h
            else:
                self.z2 = self.z2 + u_h

        if u_v > 0:
            h_r = {"needed": u_v + 1 - self.h, "new": u_v + 1, "prepend": self._v_neg}
        else:
            h_r = {"needed": -u_v, "new": self.h - u_v, "prepend": not self._v_neg}
            if self._flip:
                self.z2 = self.z2 + u_v
            else:
                self.z1 = self.z1 + u_v

        return {
            "w": w_r,
            "h": h_r,
        }

    def __iter__(self):
        return it.starmap(
            self.u_coord, ((i, j) for i in range(self.h) for j in range(self.w))
        )

    def __repr__(self):
        return (
            f"Index(w={self.w},h={self.h},c1_dir={self.c1_dir},"
            + f"c2_dir={self.c2_dir},z1={self.z1},z2={self.z2})"
        )


IJ_INDEX = {"c1_dir": Dir.D, "c2_dir": Dir.R}
XY_INDEX = {"c1_dir": Dir.R, "c2_dir": Dir.U}
XD_INDEX = {"c1_dir": Dir.R, "c2_dir": Dir.D}


def ZERO(c1, c2):
    return {"z1": c1, "z2": c2}


def add_dir(d, c1, c2, n=1, index=IJ_INDEX):
    c1_new = c1
    c1_dir = index["c1_dir"]
    if not d.ortho(c1_dir):
        if d == c1_dir:
            c1_new += n
        else:
            c1_new -= n
    c2_new = c2
    c2_dir = index["c2_dir"]
    if not d.ortho(c2_dir):
        if d == c2_dir:
            c2_new += n
        else:
            c2_new -= n
    return (c1_new, c2_new)


class Grid:
    def __init__(self, arr, index_args=IJ_INDEX):
        self.arr = arr
        self._index = Index(len(arr), len(arr[0]), **index_args)

    @property
    def w(self):
        return self._index.w

    @property
    def h(self):
        return self._index.h

    def inbounds(self, c1, c2):
        return self._inbounds(*self._index.g_coord(c1, c2))

    def _inbounds(self, i, j):
        return i >= 0 and i < self._index.h and j >= 0 and j < self._index.w

    def get(self, c1, c2, default=None, resize=False):
        i, j = self._index.g_coord(c1, c2)
        if self._inbounds(i, j):
            return self.arr[i][j]
        else:
            if resize:
                self.resize_to_idx(c1, c2, default=default)
            return default

    def set(self, c1, c2, x, default=None, resize=False):
        self.update(c1, c2, lambda _: x, default=default, resize=resize)

    def update(self, c1, c2, f, default=None, resize=False):
        i, j = self._index.g_coord(c1, c2)
        if self._inbounds(i, j):
            c = self.arr[i][j]
            self.arr[i][j] = f(c)
        elif resize:
            # use u_coords for resize & update
            self.resize_to_idx(c1, c2, default=default)
            self.update(c1, c2, f, default=default, resize=False)

    def resize_to_idx(self, c1, c2, default=None):
        resize_actions = self._index.resize(c1, c2)
        if (w_needed := resize_actions["w"]["needed"]) > 0:
            for row in self.arr:
                if resize_actions["w"]["prepend"]:
                    row[0:0] = [default] * w_needed
                else:
                    row.extend([default] * w_needed)
            self._index.w = resize_actions["w"]["new"]
        if (h_needed := resize_actions["h"]["needed"]) > 0:
            if resize_actions["h"]["prepend"]:
                self.arr[0:0] = [[default] * self._index.w for _ in range(h_needed)]
            else:
                self.arr.extend([[default] * self._index.w for _ in range(h_needed)])
            self._index.h = resize_actions["h"]["new"]

    @classmethod
    def filled(cls, w, h, default=None):
        return cls([[default] * w for _ in range(h)])

    @classmethod
    def from_str(cls, s, chr_to_v=lambda c: c):
        lines = None
        if isinstance(s, str):
            lines = s.split("\n")
        else:
            # assuming this is an iter of strs, one per row
            lines = s

        return cls([[chr_to_v(c) for c in row] for row in lines])

    def enumerate_iter(self):
        return ((idx, self.get(*idx)) for idx in self._index)

    def __iter__(self):
        return (self.get(*idx) for idx in self._index)

    def __repr__(self):
        return f"{self.__class__.__name__}(_index={self._index},arr={self.arr})"

    def __str__(self):
        return self.pprint()

    def pprint(self, h_join="", v_join="\n", v_to_chr=str):
        return v_join.join(map(h_join.join, map(lambda r: map(v_to_chr, r), self.arr)))


class XYGrid(Grid):
    def __init__(self, arr):
        super().__init__(arr, XY_INDEX)


class XDGrid(Grid):
    def __init__(self, arr):
        super().__init__(arr, XD_INDEX)

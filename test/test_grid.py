import unittest
import os
import sys
import itertools as it

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from util.grid import Grid, XYGrid, XDGrid
import util.grid as grid

test_grid_str = """..#..
.#...
#....
.##..
...##"""
test_grid_arr = [
    [".", ".", "#", ".", "."],
    [".", "#", ".", ".", "."],
    ["#", ".", ".", ".", "."],
    [".", "#", "#", ".", "."],
    [".", ".", ".", "#", "#"],
]


def msg_f(msg, g):
    return f"{msg}\n{g=}\n{g}"


class TestGrid(unittest.TestCase):
    def test_str(self):
        g = Grid.from_str(test_grid_str)
        self.assertEqual(type(g), Grid)
        self.assertEqual(g.arr, test_grid_arr)

    def test_filled(self):
        g = Grid.filled(5, 5, ".")
        self.assertEqual(type(g), Grid)
        self.assertEqual(g.arr, [["."] * 5 for _ in range(5)])

    def test_get_basic(self):
        g = Grid.from_str(test_grid_str)
        self.assertEqual(g.get(0, 2), "#", msg=msg_f("get(0, 2)", g))
        self.assertEqual(g.get(2, 4), ".", msg=msg_f("get(2, 4)", g))
        self.assertEqual(g.get(3, 2), "#", msg=msg_f("get(3, 2)", g))

    def test_get_default(self):
        g = Grid.from_str(test_grid_str)
        self.assertEqual(
            g.get(0, 2, default="?"), "#", msg=msg_f("get(0, 2, default=?)", g)
        )
        self.assertEqual(
            g.get(4, 5, default="?"), "?", msg=msg_f("get(4, 5, default=?)", g)
        )
        self.assertEqual(g.get(5, 2), None, msg=msg_f("get(5, 2)", g))

    def test_get_resize(self):
        g = Grid.filled(1, 1, ".")
        self.assertEqual(g.get(3, 4), None)
        oob_get = g.get(3, 4, default="+", resize=True)
        self.assertEqual(
            oob_get, "+", msg=msg_f("get(3, 4, default=" + ", resize=True)", g)
        )
        self.assertEqual(g.w, 5, msg=msg_f("width", g))
        self.assertEqual(g.h, 4, msg=msg_f("width", g))
        self.assertEqual(str(g), ".++++\n+++++\n+++++\n+++++")

    def test_set_basic(self):
        g = Grid.from_str(test_grid_str)
        g.set(0, 4, "!")
        new_grid_str = test_grid_str[0:4] + "!" + test_grid_str[5:]
        self.assertEqual(str(g), new_grid_str)

    def test_set_resize(self):
        g = Grid.filled(1, 1, ".")
        g.set(3, 4, "!")
        self.assertEqual(str(g), ".")
        g.set(3, 4, "!", default="+", resize=True)
        self.assertEqual(str(g), ".++++\n+++++\n+++++\n++++!")

    def test_enumerate_iter(self):
        g = Grid.from_str(test_grid_str)

        correct = iter(filter(lambda c: c != "\n", test_grid_str))
        for idx, x in g.enumerate_iter():
            self.assertEqual(g.get(*idx), x, msg=msg_f(f"get(*{idx}) != x", g))
            self.assertEqual(
                x, next(correct), msg=msg_f(f"item not correct at {idx=}", g)
            )

    def test_iter(self):
        g = Grid.from_str(test_grid_str)

        correct = iter(filter(lambda c: c != "\n", test_grid_str))
        for x in g:
            self.assertEqual(x, next(correct))


class TestXYGrid(unittest.TestCase):
    def test_str(self):
        g = XYGrid.from_str(test_grid_str)
        self.assertEqual(type(g), XYGrid)
        self.assertEqual(g.arr, test_grid_arr)

    def test_filled(self):
        g = XYGrid.filled(5, 5, ".")
        self.assertEqual(type(g), XYGrid)
        self.assertEqual(g.arr, [["."] * 5 for _ in range(5)])

    def test_get_basic(self):
        g = XYGrid.from_str(test_grid_str)
        self.assertEqual(g.get(2, 4), "#", msg=msg_f("get(2,4)", g))
        self.assertEqual(g.get(4, 2), ".", msg=msg_f("get(4,2)", g))
        self.assertEqual(g.get(2, 1), "#", msg=msg_f("get(2,1)", g))

    def test_get_default(self):
        g = XYGrid.from_str(test_grid_str)
        self.assertEqual(g.get(2, 4, default="?"), "#", msg=msg_f("get(2,4,d=?)", g))
        self.assertEqual(g.get(4, 5, default="?"), "?", msg=msg_f("get(4,5,d=?)", g))
        self.assertEqual(g.get(5, 2), None, msg=msg_f("get(5,2)", g))

    def test_get_resize(self):
        g = XYGrid.filled(1, 1, ".")
        self.assertEqual(g.get(3, 4), None)
        oob_get = g.get(3, 4, default="+", resize=True)
        self.assertEqual(oob_get, "+", msg=msg_f("get(3,4,d=+,resize)", g))
        self.assertEqual(g.w, 4, msg=msg_f("width", g))
        self.assertEqual(g.h, 5, msg=msg_f("height", g))
        self.assertEqual(str(g), "++++\n++++\n++++\n++++\n.+++")

    def test_set_basic(self):
        g = XYGrid.from_str(test_grid_str)
        g.set(0, 4, "!")
        new_grid_str = "!" + test_grid_str[1:]
        self.assertEqual(str(g), new_grid_str)

    def test_set_resize(self):
        g = XYGrid.filled(1, 1, ".")
        g.set(3, 4, "!")
        self.assertEqual(str(g), ".")
        g.set(3, 4, "!", default="+", resize=True)
        self.assertEqual(str(g), "+++!\n++++\n++++\n++++\n.+++")

    def test_enumerate_iter(self):
        g = XYGrid.from_str(test_grid_str)

        correct, correct_copy = it.tee(it.chain.from_iterable(test_grid_arr))
        correct_l = list(correct_copy)
        for idx, x in g.enumerate_iter():
            self.assertEqual(
                g.get(*idx), x, msg=msg_f(f"get(*{idx}) != x\ncorrect={correct_l}", g)
            )
            self.assertEqual(
                x,
                next(correct),
                msg=msg_f(f"item not correct at {idx=}\ncorrect={correct_l}", g),
            )

    def test_iter(self):
        g = XYGrid.from_str(test_grid_str)

        correct = it.chain.from_iterable(test_grid_arr)
        for x in g:
            self.assertEqual(x, next(correct))


class TestXDGrid(unittest.TestCase):
    def test_str(self):
        g = XDGrid.from_str(test_grid_str)
        self.assertEqual(type(g), XDGrid)
        self.assertEqual(g.arr, test_grid_arr)

    def test_filled(self):
        g = XDGrid.filled(5, 5, ".")
        self.assertEqual(type(g), XDGrid)
        self.assertEqual(g.arr, [["."] * 5 for _ in range(5)])

    def test_get_basic(self):
        g = XDGrid.from_str(test_grid_str)
        self.assertEqual(g.get(2, 0), "#", msg=msg_f("get(2,0)", g))
        self.assertEqual(g.get(4, 2), ".", msg=msg_f("get(4,2)", g))
        self.assertEqual(g.get(2, 3), "#", msg=msg_f("get(2,3)", g))

    def test_get_default(self):
        g = XDGrid.from_str(test_grid_str)
        self.assertEqual(g.get(2, 0, default="?"), "#", msg=msg_f("get(2,4,d=?)", g))
        self.assertEqual(g.get(4, 5, default="?"), "?", msg=msg_f("get(4,5,d=?)", g))
        self.assertEqual(g.get(5, 2), None, msg=msg_f("get(5,2)", g))

    def test_get_resize(self):
        g = XDGrid.filled(1, 1, ".")
        self.assertEqual(g.get(3, 4), None)
        oob_get = g.get(3, 4, default="+", resize=True)
        self.assertEqual(oob_get, "+", msg=msg_f("get(3,4,d=+,resize)", g))
        self.assertEqual(g.w, 4, msg=msg_f("width", g))
        self.assertEqual(g.h, 5, msg=msg_f("height", g))
        self.assertEqual(str(g), ".+++\n++++\n++++\n++++\n++++")

    def test_set_basic(self):
        g = XDGrid.from_str(test_grid_str)
        g.set(0, 0, "!")
        new_grid_str = "!" + test_grid_str[1:]
        self.assertEqual(str(g), new_grid_str)

    def test_set_resize(self):
        g = XDGrid.filled(1, 1, ".")
        g.set(3, 4, "!")
        self.assertEqual(str(g), ".")
        g.set(3, 4, "!", default="+", resize=True)
        self.assertEqual(str(g), ".+++\n++++\n++++\n++++\n+++!")

    def test_enumerate_iter(self):
        g = XDGrid.from_str(test_grid_str)

        correct, correct_copy = it.tee(it.chain.from_iterable(test_grid_arr))
        correct_l = list(correct_copy)
        for idx, x in g.enumerate_iter():
            self.assertEqual(
                g.get(*idx), x, msg=msg_f(f"get(*{idx}) != x\ncorrect={correct_l}", g)
            )
            self.assertEqual(
                x,
                next(correct),
                msg=msg_f(f"item not correct at {idx=}\ncorrect={correct_l}", g),
            )

    def test_iter(self):
        g = XDGrid.from_str(test_grid_str)

        correct = it.chain.from_iterable(test_grid_arr)
        for x in g:
            self.assertEqual(x, next(correct))


class TestRelativeGrid(unittest.TestCase):
    def test_negative(self):
        g = Grid([["."]])

        for i in range(5):
            g.set(i, 0, "#", default=".", resize=True)

        self.assertEqual(
            str(g), "#\n#\n#\n#\n#", msg=msg_f("set i 0 to 4 str check failed", g)
        )

        for j in range(0, -5, -1):
            g.set(i, j, "#", default=".", resize=True)

        self.assertEqual(
            str(g),
            "....#\n....#\n....#\n....#\n#####",
            msg=msg_f("set j 0 to -4 str check failed", g),
        )

        g.set(-1, 1, "!", default=".", resize=True)
        self.assertEqual(
            str(g),
            ".....!\n....#.\n....#.\n....#.\n....#.\n#####.",
            msg=msg_f("set -1,1 str check failed", g),
        )

    def test_relative(self):
        g = Grid([["+"]], index_args=(grid.XY_INDEX | grid.ZERO(10, 0)))

        for x, y in zip(range(11, 15), range(1, 5)):
            g.set(x, y, "/", default=".", resize=True)
        self.assertEqual(
            str(g),
            "..../\n.../.\n../..\n./...\n+....",
            msg=msg_f("set diag right str check failed", g),
        )
        for x, y in zip(reversed(range(6, 10)), range(1, 5)):
            g.set(x, y, "\\", default=".", resize=True)
        self.assertEqual(
            str(g),
            "\......./\n.\...../.\n..\.../..\n...\./...\n....+....",
            msg=msg_f("set diag right str check failed", g),
        )


if __name__ == "__main__":
    unittest.main()

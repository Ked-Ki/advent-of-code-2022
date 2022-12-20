import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.day15 import RangeSet


class TestRangeSet(unittest.TestCase):
    def test_insert(self):
        r_set = RangeSet()
        self.assertEqual(r_set.arr, [], msg="empty set")

        r_set.insert((5, 10))
        self.assertEqual(r_set.arr, [5, 10], msg="insert first range")

        r_set.insert((15, 20))
        self.assertEqual(r_set.arr, [5, 10, 15, 20], msg="insert disjoint range")

        r_set.insert((16, 18))
        self.assertEqual(r_set.arr, [5, 10, 15, 20], msg="insert interior range")

        r_set.insert((4, 6))
        self.assertEqual(r_set.arr, [4, 10, 15, 20], msg="insert left extend range")

        r_set.insert((19, 24))
        self.assertEqual(r_set.arr, [4, 10, 15, 24], msg="insert right extend range")

        r_set.insert((6, 16))
        self.assertEqual(r_set.arr, [4, 24], msg="insert merging range")

    def test_iter(self):
        r_set = RangeSet()

        ranges = [(-1, 3), (5, 10), (15, 20)]

        for rng in ranges:
            r_set.insert(rng)

        self.assertEqual(list(r_set), ranges)

    def test_size(self):
        r_set = RangeSet()

        r_set.insert((5, 10))  # 6
        r_set.insert((15, 20))  # 6
        r_set.insert((-1, 3))  # 5

        self.assertEqual(r_set.size(), 17, msg="size")

    def test_equal_bounds(self):
        r_set = RangeSet()

        r_set.insert((-2, 14))
        r_set.insert((16, 24))
        self.assertEqual(r_set.arr, [-2, 14, 16, 24], msg="setup")

        r_set.insert((14, 18))
        self.assertEqual(r_set.arr, [-2, 24], msg="equal left range should have merged")

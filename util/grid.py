class Grid:
    def __init__(self, arr):
        self.arr = arr
        self.w = len(arr[0])
        self.h = len(arr)

    def inbounds(self, i, j):
        return i >= 0 and i < self.h and j >= 0 and j < self.w

    def get(self, i, j, default=None):
        if self.inbounds(i,j):
            return self.arr[i][j]
        else:
            return default

    def set(self, i, j, x):
        self.update(i, j, lambda _: x)

    def update(self, i, j, f):
        if self.inbounds(i,j):
            c = self.arr[i][j]
            self.arr[i][j] = f(c)

    @staticmethod
    def filled(w, h, default=None):
        return Grid([[default] * w for _ in range(h)])

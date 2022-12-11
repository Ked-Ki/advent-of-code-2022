class ReprFunc:
    def __init__(self, func, name):
        self.func = func
        self.name = name

    def __call__(self, v):
        return self.func(v)

    def __repr__(self):
        return self.name

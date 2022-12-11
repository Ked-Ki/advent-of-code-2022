import collections

def consume(it):
    collections.deque(it, maxlen=0)

def batch_at(it, is_new):
    transition = [next(it)]
    done = False
    while not done:
        def batch_iter():
            for i in it:
                if not is_new(i):
                    yield i
                else:
                    transition.append(i)
                    return
            nonlocal done
            done = True

        def wrapped_iter():
            nonlocal transition
            yield from transition
            transition = []
            yield from batch_iter()

        yield wrapped_iter()
    return

def takewhile_inclusive(pred, it):
    bound = []
    for i in it:
        if pred(i):
            yield i
        else:
            yield i
            break

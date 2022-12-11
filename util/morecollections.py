def consume_deque(d, from_left=False):
    done = False
    while not done:
        try:
            if from_left:
                yield d.popleft()
            else:
                yield d.pop()
        except IndexError:
            break

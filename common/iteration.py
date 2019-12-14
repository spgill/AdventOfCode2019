def every(iterable, n):
    """Yield groups of `n` size from iterable"""
    assert len(iterable) % n == 0
    stack = list()
    for i in iterable:
        stack.append(i)
        if len(stack) == n:
            yield tuple(stack)
            stack = list()

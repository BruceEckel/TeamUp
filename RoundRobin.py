from collections import deque

def round_robin_even(d, n):
    for i in range(n - 1):
        yield [[d[j], d[-j-1]] for j in range(n/2)]
        d[0], d[-1] = d[-1], d[0]
        d.rotate()

def round_robin_odd(d, n):
    for i in range(n):
        h = [[d[j], d[-j-1]] for j in range(n/2)]
        h[-1].append(d[n/2])
        yield h
        d.rotate()

def round_robin(n):
    d = deque(range(n))
    if n % 2 == 0:
        return list(round_robin_even(d, n))
    else:
        return list(round_robin_odd(d, n))

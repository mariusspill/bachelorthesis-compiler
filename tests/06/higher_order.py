
def map(f: Callable[[int], int], t: tuple[int, int]) -> tuple[int, int]:
    return f(t[0]), f(t[1])

def inc(x: int) -> int:
    return x + 1

y = map(inc, (1, 2))
print(y[0])
print(y[1])

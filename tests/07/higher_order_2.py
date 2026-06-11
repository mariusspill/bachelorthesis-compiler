def map(f: Callable[[int], int], t: tuple[int, int]) -> tuple[int, int]:
    return f(t[0]), f(t[1])
t1 = (10, 100)
t2 = map(lambda x: x + 1, t1)
print(t1[0])
print(t1[1])
print(t2[0])
print(t2[1])

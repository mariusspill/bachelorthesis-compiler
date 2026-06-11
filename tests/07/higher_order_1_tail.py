def apply_to_10(f: Callable[[int], int]) -> int:
    return f(10)
print(apply_to_10(lambda x: x + 20))

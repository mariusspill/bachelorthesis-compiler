def apply_to_10_2(f: Callable[[float], float]) -> float:
    return f(10.2)
print(apply_to_10_2(lambda x: x + 20.0))


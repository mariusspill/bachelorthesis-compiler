def truth() -> int:
    return 42

def func(x: int) -> bool:
    return True if x == truth() else False

print(42 if func(input_int()) else 0)

def make_adder(x: float) -> Callable[[float], float]:
    return lambda y: x + y

add1 = make_adder(1.1)
add2 = make_adder(2.2)
add3 = make_adder(3.3)

result = add1(add2(add3(0.0)))
print(result)

def foo() -> int:
    class Foo:
        bar: int

    f = Foo(5)
    return f.bar

print(foo())
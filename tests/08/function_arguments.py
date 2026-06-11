class RGB:
    red: int
    green: int
    blue: int


def intensity(v: RGB) -> int:
    return v.red + v.green + v.blue



r = RGB(100, 24, 0)
print(intensity(r))

class RGB:
    red: int
    green: int
    blue: int

class Color:
    rgb: RGB
    luminance: int


def intensity(v: RGB) -> int:
    return v.red + v.green + v.blue

def cintensity(c: Color) -> int:
    # This of course makes no sense at all, but works for testing :)
    return intensity(c.rgb) + c.luminance


r = RGB(100, 24, 0)
c = Color(r, 100)
print(intensity(r))
print(cintensity(c))


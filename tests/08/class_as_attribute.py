class RGB:
    red: int
    green: int
    blue: int

class Pixel:
    color: RGB
    brightness: int

p = Pixel(RGB(10,12,15), 50)
print(p.color.red)
print(p.color.green)
print(p.color.blue)
print(p.brightness)
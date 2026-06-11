class Vector3D:
    x: int
    y: int
    z: int

class RGB:
    red: int
    green: int
    blue: int

class Color:
    rgb: RGB
    luminance: int

class Light:
    position: Vector3D
    direction: Vector3D
    color: Color

def r_intensity(r: RGB) -> int:
    return r.red + r.green + r.blue

def c_intensity(c: Color) -> int:
    return r_intensity(c.rgb) + c.luminance

def l_intensity(l: Light) -> int:
    return c_intensity(l.color)

def v_add(a: Vector3D, b: Vector3D) -> Vector3D:
    return Vector3D(a.x + b.x, a.y + b.y, a.z + b.z)

def v_print(v: Vector3D) -> int:
    print(v.x)
    print(v.y)
    print(v.z)
    return 0

def l_target(l: Light) -> Vector3D:
    return v_add(l.position, l.direction)


pos = Vector3D(10, 20, 30)
dir = Vector3D(3, 2, 1)
rgb = RGB(100, 24, 0)
col = Color(rgb, 100)
lig = Light(pos, dir, col)

print(r_intensity(rgb))
print(c_intensity(col))
print(l_intensity(lig))
print(0)
v_print(l_target(lig))


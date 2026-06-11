x = input_int() # 42
y = input_int() # 0
u = x == y # false
v = x != y # true

if not (u and v):
    z = x - y
else:
    z = 0
print(z)

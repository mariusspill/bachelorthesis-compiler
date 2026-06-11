a = (42, 42, 42, 42, 42, 42, (0, 42))
b = input_int()
c = (b, 13)
if a[6][1] == c[0]:
    print(a[0] + c[1])
else:
    print(0)

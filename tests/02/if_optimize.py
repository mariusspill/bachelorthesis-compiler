if True:
    y = input_int()
else:
    if input_int() == 0:
        y = 777
    else:
        y = 1 + input_int()
print(y + 2)

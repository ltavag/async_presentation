def foo():
    x = gen1()
    return lambda: x.__next__()


def gen1():
    for i in range(0, 5):
        yield i


y = foo()

print(y())
print(y())
print(y())
print(y())
print(y())
print(y())
print(y())

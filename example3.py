import traceback


def foo():
    x = gen1()
    return lambda: x.__next__()


def gen1():
    for i in range(0, 5):
        traceback.print_stack()
        yield i


y = foo()

print(y())
print(y())
print(y())
print(y())
print(y())
print(y())
print(y())

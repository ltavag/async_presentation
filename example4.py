def foo():
    x = gen1()
    return lambda y: x.send(y)


def gen1():
    for i in range(0, 9):
        x = yield i
        print(x)
        print(i)


y = foo()

y(None)
y('Hey')
y('I')
y('just')
y('met')
y('you')
y('and')
y('this')
y('is')
y('crazy')

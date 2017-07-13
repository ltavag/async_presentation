import traceback

def foo():
  x = gen1()
  return lambda: x.next()

def gen1():
  for i in xrange(0,5):
    traceback.print_stack()
    yield i

y = foo()

print y()
print y()
print y()
print y()
print y()
print y()

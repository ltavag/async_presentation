import traceback

def foo():
  bar()

def bar():
  traceback.print_stack()

foo()

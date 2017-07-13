import sys 

def grep(pattern):
  print("Searching for", pattern)
  while True:
    line = (yield)
    if pattern in line:
      print(line)

g = grep('def')
g.send(None)
for line in sys.stdin:
  g.send(line)

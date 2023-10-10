import sys

from math import hypot

lines = []
for line in sys.stdin:
  lines.append(line.rstrip('\n'))
  
s = 0
for xy in lines[1:]:
    x, y = map(int, xy.split())
    if hypot(x, y) < 100:
        s += 1

print(s)
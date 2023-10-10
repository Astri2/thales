import sys
import re

lines = []
for line in sys.stdin:
  lines.append(line.rstrip('\n'))


for i,s in enumerate(lines[1:]):
    p = re.compile("^" + s.replace("_", ".") + "$")
    if p.match("ALIMENTATION"):
        print(i+1)
        exit()
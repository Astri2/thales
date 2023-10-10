import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

hours = []
for s in lines[1:]:
    a, b = s.split(" - ")
    a = int(a.split(":")[0]) * 60 + int(a.split(":")[1])
    b = int(b.split(":")[0]) * 60 + int(b.split(":")[1])

    hours.append((a, b, b-a))

def overlap(a, b):
    if a[2] < 15 or b[2] < 15: return 0

    if a[0] == b[0]:
        return min(a[2], b[2]) >= 15
    
    elif a[0] <= b[0] <= a[1]:
        dt = b[0]-a[0]     
        return a[2]-dt >= 15
    
    elif b[0] <= a[0] <= b[1]:
        dt = a[0]-b[0]
        return b[2]-dt >= 15

    return 0


c = 0
for i, eltA in enumerate(hours[:-1]):
    j=i+1
    for eltB in hours[i+1:]:
        # print(i,j)
        s = overlap(eltA,eltB)
        c += s
        j+=1
print(c)
class T:
    minlen = 999999999

def recouvre(s1, s2):
    recouv_max = min(len(s1),len(s2))
    for recouv in range(recouv_max,0,-1):
        if s1[-recouv:] == s2[:recouv]: 
            return s1[:-recouv] + s2
    return s1+s2

def generate_table(s, i):
    if len(s) >= T.minlen: return []
    
    if i == len(lines): 
        T.minlen = len(s)
        return [s]

    possibilites = []
    genes = lines[i]
    ng = genes[::-1]
    possibilites += generate_table(recouvre(s, genes), i+1)
    possibilites += generate_table(recouvre(s, ng), i+1)
    return possibilites

input()
lines = input().split()
p = generate_table(lines[0], 1) + generate_table(lines[0][::-1], 1)
p.sort(key=len)
print(p[0])
from read_input import Instance, Solution

inst = Instance.from_argv()

path_lengths = []
for p in inst.paths:
    l = 0
    for s in p:
        l += inst.streets[s][2]
    path_lengths.append((l,p))

path_lengths.sort()

streets_visited = set()
intersections = [[None]*inst.D for _ in range(inst.I)]
for l,p in path_lengths:
    if any(s in streets_visited for s in p): continue
    streets_visited.update(p)

    t = 0
    for ctr,s in enumerate(p):
        if ctr > 0: t += inst.streets[s][2]
        e = inst.streets[s][1]
        while intersections[e][t] != None: t += 1
        intersections[e][t] = s

sol = []
for i,isn in enumerate(intersections):
    print(i, '/', len(intersections), '     ', end = '\r')
    if list(filter(lambda x : x != None, isn)):
        for a in isn:
            if a != None:
                s = a
                break
        res = []
        t = -1
        for x,a in enumerate(isn):
            if a != None and a != s:
                res.append((s,x-t))
                t = x
                s = a
        res.append((s,inst.D-t-1))

        already_present = set()
        for a,b in res:
            if a in already_present:
                print(res)
                sys.exit()
            already_present.add(a)
        sol.append((i,res))

print(sol)
s = Solution(sol, inst)
s.write()

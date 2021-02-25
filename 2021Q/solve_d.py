from read_input import Instance, Solution
import sys

inst = Instance.from_argv()

from collections import defaultdict
streets = defaultdict(int)
for path in inst.paths:
    for street in path:
        streets[street] += 1

new_streets = {}
for street in streets:
    new_streets[street] = inst.streets[street]

inst.streets = new_streets

graph = {}
for s,(b,e,l) in inst.streets.items():
    if e not in graph: graph[e] = set()
    graph[e].add(b)

path_lengths = []
for p in inst.paths:
    l = 0
    for s in p:
        l += inst.streets[s][2]
    path_lengths.append((l,p))
path_lengths.sort(reverse = True)

m = float(sys.argv[2]) if len(sys.argv) >= 3 else 1
print("Multiplier:", m)
epochs = [round(m * (len(graph[e]) if e in graph else 1)) for e in range(inst.I)]

intersections = [[None]*epochs[e] for e in range(inst.I)]
fitted_streets = [{} for _ in range(inst.I)]
for i,(l,p) in enumerate(path_lengths):
    print(i, '/', len(path_lengths), '    ', end = '\r')
    t = 0
    to_add = set()
    for ctr,s in enumerate(p):
        if ctr > 0: t += inst.streets[s][2]
        e = inst.streets[s][1]
        if s in fitted_streets[e]:
            t += ((fitted_streets[e][s] - t)%epochs[e] + epochs[e])%epochs[e]
            if t >= inst.D: break
        else:
            while intersections[e][t%epochs[e]] != None and t < inst.D:
                t += 1
            if t == inst.D: break
            to_add.add((e,t%epochs[e],s))
    else:
        for e,t,s in to_add:
            intersections[e][t] = s
            fitted_streets[e][s] = t

sol = []
for i,isn in enumerate(intersections):
    print(i, '/', len(intersections), '     ', end = '\r')
    if list(filter(lambda x : x != None, isn)):
        for a in isn:
            if a != None:
                s = a
                break
        res = []
        t = 0
        for x,a in enumerate(isn):
            if a != None and a != s:
                res.append((s,x-t))
                t = x
                s = a
        res.append((s,epochs[i]-t))
        if any(b == 0 for a,b in res):
            print(res)
            sys.exit()
        if sum(b for a,b in res) != epochs[i]:
            print(res)
            sys.exit()

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

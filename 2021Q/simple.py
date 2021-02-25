from read_input import Instance, Solution

inst = Instance.from_argv()

intersection_counts = [{} for _ in range(inst.I)]
for p in inst.paths:
    for s in p[:-1]:
        if s not in intersection_counts[inst.streets[s][1]]: intersection_counts[inst.streets[s][1]][s] = 0
        intersection_counts[inst.streets[s][1]][s] += 1

sol = []
epoch_length = 10
for i,intsctn in enumerate(intersection_counts):
    tot = sum(intsctn.values())
    durs = []
    for s,n in intsctn.items():
        durs.append((s,round(tot/n * epoch_length)))
    sol.append((i,durs))

s = Solution(sol, inst)
s.write()

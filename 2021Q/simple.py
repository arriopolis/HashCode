from read_input import Instance, Solution

inst = Instance.from_argv()
sol = Solution()

intersection_counts = [{} for _ in range(inst.I)]
for p in inst.paths:
    for s in p[:-1]:
        if s not in intersection_counts[inst.streets[s][1]]: intersection_counts[inst.streets[s][1]][s] = 0
        intersection_counts[inst.streets[s][1]][s] += 1

print(intersection_counts)

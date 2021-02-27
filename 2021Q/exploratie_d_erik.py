from read_input import Instance, Solution
from collections import defaultdict


inst = Instance.from_argv()

print(inst)

print()


# Veel straten
# alle autos hebben 200 straten (eigen pad?)

paths = set()
for path in inst.paths:
    path_hash = ";;".join(path)
    if path_hash in paths:
        print(path_hash)
    paths.add(path_hash)

# Hyp: alle paden hebben unieke straten


streets = defaultdict(int)
for path in inst.paths:
    for street in path:
        streets[street] += 1


new_streets = {}
for street in streets:
    new_streets[street] = inst.streets[street]

inst.streets[street] = new_streets

print(len(streets))

street_iid = defaultdict(list)



for street in streets:
    street_iid[inst.streets[street][1]].append(street)

sol = [(iid, [(street,1)for street in streets]) for iid, streets in street_iid.items()]

Solution(sol,inst).write()
sys.exit()

#Hyp : De tijd van de auto is precies D
times = []

upperbound = 0
for path in inst.paths:
    time = 0
    for street in path[1:]:
        time += inst.streets[street][2]
    times.append(time)
    if time <= inst.D:
        upperbound += inst.F + (inst.D-time)
print(upperbound)
sys.exit()


#print(sorted(times))

# Aantal straten per intersectie
street_per_int = defaultdict(int)

for street in streets.keys():
    street_per_int[inst.streets[street][1]] +=1


# street feasibility

street_feasible = defaultdict(list)


for path in inst.paths:
    times = {}
    time = 0
    for street in path:
        time += inst.streets[street][2]
        times[street] = time

    time = inst.D
    for street in path:
        times[street] =(times[street],time)
        time -= inst.streets[street][2]

    for street, interval in times.items():
        street_feasible[street] += [times[street]]

for street in streets:
    _min = 0
    _max = inst.D
    for interval in street_feasible[street]:
        _min = max(interval[0], _min)
        _max = min(interval[1], _max)
    if street_per_int[inst.streets[street][1]]>1:
        if _min>= _max:
            print(street)




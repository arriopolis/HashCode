from read_input import Instance
import numpy as np



instance = Instance("input/e_intriguing.in")

# calculate dependencies for each target
dependencies = {
}

times ={n: (c,r) for n,c,r in instance.compiled_files}

assert len(instance.compiled_files) == len(instance.dependencies)
for file, dep in zip(instance.compiled_files, instance.dependencies):
    if len(dep) !=0:
        dependencies[file[0]] = set(dep)


#Hypothesis: Instance has depth 1
for file, dep in dependencies.items():
    for d in dep:
        assert d not in dependencies

#Hypothesis: targets have distinct dependencies
for f1, d1 in dependencies.items():
    for f2,d2 in dependencies.items():
        if f1 != f2:
            assert len(set(d1).intersection(set(d2))) == 0


# SOLUTION

# find compile time per target

def parallel_scheduler(t_server, jobs):
    scheduled = [[] for i in range(len(t_server))]
    for job in sorted(jobs, key = lambda x: x[1])[::-1]:
        i_server = np.argmin(t_server)
        scheduled[i_server].append(job[0])
        t_server[i_server] += job[1]
    return scheduled, t_server


schedules = {}
for target_name, (deadline,score)  in instance.target_files_dict.items():
    print("----",target_name, deadline, score,"-----")
    jobs = [(d,instance.compiled_files_dict[d][0]) for d in dependencies[target_name]]
    schedule, t_server = parallel_scheduler([0]*3, jobs)
    print(int(deadline) - max(t_server), int(deadline)-sum(t_server)/3, len(jobs))
    schedules[target_name] = schedule

# Conclusion: Only one target can be reached properly So we should take the biggest
from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')

n_bins = 3

x = {}
for job in jobs:
    for b in range(n_bins):
        x[(job[0], b)] = solver.IntVar(0, 1, 'x_%s_%i' % (job[0], b))

for job in jobs:
    solver.Add(sum(x[job[0], b] for b in range(n_bins)) == 1)


for b in range(n_bins):
    solver.Add(
        sum(x[(job[0],b)]*job[1]
            for job in jobs) <= int(deadline)-1001)


objective = solver.Objective()

for job in jobs:
    for b in range(n_bins):
        objective.SetCoefficient(x[(job[0], b)], 1)
objective.SetMaximization()

status = solver.Solve()
print(status)

schedule = [list() for i in range(n_bins)]

if status == pywraplp.Solver.OPTIMAL:
    print(objective.Value())

    for job in jobs:
        for b in range(n_bins):
            if x[job[0], b].solution_value() ==1:
                schedule[b] +=[job[0]]

    print("found")
else:
    print('The problem does not have an optimal solution.')

for s in schedule:
    print(sum([instance.compiled_files_dict[fn][0]for fn in s]))

schedule[2]+=[target_name]

jobs =[]

from read_output import Solution
solution = Solution()
solution.E = sum([len(s) for s in schedule])
solution.compilation_steps = [ (fn,i)
    for i, s in enumerate(schedule) for fn in s
]

print(solution.determine_score(instance))


import sys
jobs = [ (fn,i)
    for i, s in enumerate(schedule) for fn in s
]
with open('res/{}_{}.txt'.format('e_intriguing', score), 'w') as f:
    f.write(str(len(jobs)) + '\n')
    for name,s in jobs:
        f.write('{} {}\n'.format(name, s))


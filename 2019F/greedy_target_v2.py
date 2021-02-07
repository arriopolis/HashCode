import sys
from read_input import Instance

inst = Instance(sys.argv[1])

compile_times = {name : c for name,c,_ in inst.compiled_files}
replicate_times = {name : r for name,_,r in inst.compiled_files}
target_files = {name : (d,g) for name,d,g in inst.target_files}
dep_graph = {name : set() for name,_,_ in inst.compiled_files}
child_graph = {name : set() for name,_,_ in inst.compiled_files}

for i,deps in enumerate(inst.dependencies):
    name = inst.compiled_files[i][0]
    for d in deps:
        dep_graph[name].add(d)
        child_graph[d].add(name)

# Prune non-useful parts of the tree
useful_dep_graph = {}
useful_child_graph = {}
to_visit = set(target_files)
while to_visit:
    name = to_visit.pop()
    useful_dep_graph[name] = dep_graph[name]
    for x in dep_graph[name]:
        if x not in useful_child_graph: useful_child_graph[x] = set()
        useful_child_graph[x].add(name)
        if x not in useful_dep_graph:
            to_visit.add(x)

dep_graph,child_graph = useful_dep_graph,useful_child_graph

# Set up lower bound data structure
print("Setting up lower bounds...")
lower_bounds = {}
prev_files = {}
frontier = set(x for x,deps in dep_graph.items() if not deps)
while frontier:
    print(len(frontier), '    ', end = '\r')
    name = frontier.pop()

    if dep_graph[name]:
        if len(dep_graph[name]) == 1:
            prev_file = list(dep_graph[name])[0]
            lower_bound = lower_bounds[prev_file]
        else:
            lower_bound = (float('inf'),None)
            for x in dep_graph[name]:
                new_lower_bound = lower_bounds[x]
                new_lower_bound = max(new_lower_bound, max(min(lower_bounds[x] + compile_times[y], lower_bounds[y] + replicate_times[y]) for y in dep_graph[name] if y != x))
                lower_bound = min(lower_bound, (new_lower_bound, x))
            lower_bound,prev_file = lower_bound
    else:
        lower_bound = 0
        prev_file = None
    lower_bounds[name] = lower_bound + compile_times[name]
    prev_files[name] = prev_file

    if name in child_graph:
        for x in child_graph[name]:
            if dep_graph[x] <= set(lower_bounds.keys()):
                frontier.add(x)
print()

# Update the data structure
print("Updating data structure...")
target_files = {name : (d,g) for name,(d,g) in target_files.items() if lower_bounds[name] <= d}
useful_dep_graph = {}
useful_child_graph = {}
to_visit = set(target_files)
while to_visit:
    name = to_visit.pop()
    useful_dep_graph[name] = dep_graph[name]
    for x in dep_graph[name]:
        if x not in useful_child_graph: useful_child_graph[x] = set()
        useful_child_graph[x].add(name)
        if x not in useful_dep_graph:
            to_visit.add(x)

dep_graph,child_graph = useful_dep_graph,useful_child_graph
print("Number of files left:", len(dep_graph))

server_available_times = [0]*inst.S
server_files_available = [{} for _ in range(inst.S)]
compiled = set()
jobs = []
score = 0
num_overdue = 0

while target_files:
    old_dep_graph,old_child_graph = dep_graph,child_graph

    target_name,(d,g) = max(target_files.items(), key = lambda x : x[1][1] + x[1][0] - lower_bounds[x[0]])
    print("Attempting to place target file:", target_name)
    print("Current score:", score)
    useful_dep_graph = {}
    useful_child_graph = {}
    to_visit = set([target_name])
    while to_visit:
        name = to_visit.pop()
        useful_dep_graph[name] = dep_graph[name]
        for x in dep_graph[name]:
            if x not in useful_child_graph: useful_child_graph[x] = set()
            useful_child_graph[x].add(name)
            if x not in useful_dep_graph:
                to_visit.add(x)
    dep_graph,child_graph = useful_dep_graph,useful_child_graph

    frontier = set(x for x,deps in dep_graph.items() if not deps)

    while frontier:
        print("Number of compiled files: {} / {}      ".format(len(compiled), len(old_dep_graph)), end = '\r')
        name = frontier.pop()
        if name not in dep_graph: continue
        best_finish_time = (float('inf'), None)
        for s in range(inst.S):
            files_available = max(server_files_available[s][x] for x in dep_graph[name]) if dep_graph[name] else 0
            start_compile = max(files_available, server_available_times[s])
            finish_time = start_compile + compile_times[name]
            best_finish_time = min(best_finish_time, (finish_time,s))
        finish_time,s = best_finish_time
        if s is None: break
        jobs.append((name,s))
        server_available_times[s] = finish_time
        server_files_available[s][name] = finish_time
        for other_s in range(inst.S):
            if other_s == s: continue
            server_files_available[other_s][name] = finish_time + replicate_times[name]
        if name in target_files:
            print("Reached target file {}, with deadline {} at time {}.".format(name, target_files[name][0], finish_time))
            if finish_time <= target_files[name][0]:
                score += target_files[name][1] + target_files[name][0] - finish_time
            else:
                num_overdue += 1
            del target_files[name]
        compiled.add(name)
        if name in child_graph:
            for x in child_graph[name]:
                if dep_graph[x] <= compiled:
                    frontier.add(x)

        to_visit = set()
        target_files_todel = set()
        if finish_time > lower_bounds[name]:
            lower_bounds[name] = finish_time
            if name in child_graph:
                for x in child_graph[name]:
                    to_visit.add(x)
        while to_visit:
            x = to_visit.pop()

            if dep_graph[x]:
                if len(dep_graph[x]) == 1:
                    lower_bound = lower_bounds[list(dep_graph[x])[0]]
                else:
                    lower_bound = float('inf')
                    for y in dep_graph[x]:
                        new_lower_bound = lower_bounds[y]
                        new_lower_bound = max(new_lower_bound, max(lower_bounds[z] + replicate_times[z] for z in dep_graph[x] if z != y))
                        lower_bound = min(lower_bound, new_lower_bound)
            else:
                lower_bound = 0
            new_lower_bound = lower_bound + compile_times[x]

            # new_lower_bound = (max(lower_bounds[y] for y in dep_graph[x]) if dep_graph[x] else 0) + compile_times[x]
            if new_lower_bound > lower_bounds[x]:
                lower_bounds[x] = new_lower_bound
                if x in child_graph:
                    for y in child_graph[x]:
                        to_visit.add(y)
                if x in target_files and lower_bounds[x] >= target_files[x][0]:
                    target_files_todel.add(x)
        if target_files_todel:
            for x in target_files_todel:
                del target_files[x]
            useful_dep_graph = {}
            useful_child_graph = {}
            to_visit = set([target_name])
            while to_visit:
                name = to_visit.pop()
                useful_dep_graph[name] = dep_graph[name]
                for x in dep_graph[name]:
                    if x not in useful_child_graph: useful_child_graph[x] = set()
                    useful_child_graph[x].add(name)
                    if x not in useful_dep_graph:
                        to_visit.add(x)
            dep_graph,child_graph = useful_dep_graph,useful_child_graph
            print()
            print("Number of files left:", len(useful_dep_graph))

    dep_graph,child_graph = old_dep_graph,old_child_graph

print()
print("Score:", score)
print("Number of items that were overdue:", num_overdue)

# score = calc_score(jobs)
# print("Score:", score)

with open('res/{}_{}.out'.format(sys.argv[1].split('/')[1][0], score), 'w') as f:
    f.write(str(len(jobs)) + '\n')
    for name,s in jobs:
        f.write('{} {}\n'.format(name, s))

# print("Number of servers:", inst.S)
# for name,deps in sorted(dep_graph.items(), key = lambda x : len(x[1]), reverse = True):
#     if name in target_files: print("TARGET!")
#     print(name,deps)

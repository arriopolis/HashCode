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

server_available_times = [0]*inst.S
server_files_available = [{} for _ in range(inst.S)]
compiled = set()
frontier = set(x for x,deps in dep_graph.items() if not deps)
jobs = []
score = 0
while frontier:
    print("Number of compiled files: {} / {}      ".format(len(compiled), len(dep_graph)), end = '\r')
    name = frontier.pop()
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
    if name in target_files and finish_time <= target_files[name][0]:
        score += target_files[name][1] + target_files[name][0] - finish_time
    compiled.add(name)
    if name in child_graph:
        for x in child_graph[name]:
            if dep_graph[x] <= compiled:
                frontier.add(x)
print()
print("Score:", score)

# score = calc_score(jobs)
# print("Score:", score)

with open('res/{}_{}.txt'.format(sys.argv[1].split('/')[1][0], score), 'w') as f:
    f.write(str(len(jobs)) + '\n')
    for name,s in jobs:
        f.write('{} {}\n'.format(name, s))

# print("Number of servers:", inst.S)
# for name,deps in sorted(dep_graph.items(), key = lambda x : len(x[1]), reverse = True):
#     if name in target_files: print("TARGET!")
#     print(name,deps)

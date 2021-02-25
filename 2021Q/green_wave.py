from read_input import Instance, Solution

inst = Instance.from_argv()

graph = {}
for s,(b,e,l) in inst.streets.items():
    if b not in graph: graph[b] = set()
    graph[b].add(e)

degs = list(map(len,graph.values()))
print(degs)
import sys
sys.exit()

ls = set()
rs = set()

visited = set()
to_visit = set([0])
l = True
while to_visit:
    new_to_visit = set()
    for x in to_visit:
        if l: ls.add(x)
        else: rs.add(x)
        visited.add(x)
        for y in graph[x]:
            if y not in visited:
                new_to_visit.add(y)
    to_visit = new_to_visit
    l = not l

for x in ls:
    if not graph[x] <= rs:
        print(graph[x].difference(rs))

assigned = set()
to_assign = set([0])
i = 0
while to_assign:
    for x in to_assign:
        assigned.add(x)

print(len(inst.streets))
# print(inst.streets)

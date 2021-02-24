from read_input import Input, Solution
from collections import defaultdict, Counter
import numpy as np
import heapq

inp = Input.from_argv()
inp.libraries = inp.libraries


book_counts = {i:len(lib[2]) for i, lib in enumerate(inp.libraries)}


libraries_per_book =defaultdict(list)

for i, library in enumerate(inp.libraries):
    for book in library[2]:
        libraries_per_book[book].append(i)

print(Counter([len(b) for b in libraries_per_book.values()]))

scores_per_unicity= defaultdict(list)



for b, lib in libraries_per_book.items():
    scores_per_unicity[len(lib)].append(inp.scores[b])

for unicity, scores in scores_per_unicity.items():
    print(unicity, np.mean(scores), np.std(scores), np.min(scores), np.max(scores))


books_in_libraries = set()

for lib in inp.libraries:
    books_in_libraries |= set(lib[2])

for book in range(inp.B):
    assert book in books_in_libraries, book



from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')

n_bins = 3

x = {}
b ={}
for lib in range(inp.L):
    x[lib] = solver.IntVar(0, 1, 'x_%i' % (lib))

for book in range(inp.B):
    b[book]= solver.IntVar(0, 1, 'b_%i' % (lib))



for book, libs in libraries_per_book.items():
    # solver.Add(
    #     sum(x[lib]
    #         for lib in libs) >=1)
    solver.Add( b[book] <= sum(x[lib]
            for lib in libs))



objective = solver.Objective()

for lib in range(inp.L):
    objective.SetCoefficient(x[lib], len(inp.libraries[lib][2]))
for book in range(inp.B):
    objective.SetCoefficient(b[book], -1)
objective.SetMinimization()

solver.EnableOutput()
status = solver.Solve()
print(status)
if status == pywraplp.Solver.OPTIMAL:
    print("done")
    print(objective.Value())
    print(sum([len(lib[2]) for lib in inp.libraries]))
    selected = []
    for l in range(inp.L):
        if (x[l].solution_value() >= .5):
            selected.append(l)
    print(len(selected))

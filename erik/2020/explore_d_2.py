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


unique_books = set()
all_books = set()
for b, lib in libraries_per_book.items():
    if len(lib) == 1:
        unique_books.add(b)
    all_books.add(b)
    scores_per_unicity[len(lib)].append(inp.scores[b])

print(len(all_books), inp.B)
for unicity, scores in scores_per_unicity.items():
    print(unicity, np.mean(scores), np.std(scores), np.min(scores), np.max(scores))


books_in_libraries = set()

for lib in inp.libraries:
    books_in_libraries |= set(lib[2])

for book in range(inp.B):
    assert book in books_in_libraries, book

n=  1
lib_version = {l:0 for l in range(inp.L)}
I = set()
picked_books = set()
i=0
s= [(-len(set(inp.libraries[lid][2])-picked_books),lid,lib_version[lid]) for lid in range(inp.L)]
heapq.heapify(s)
while len(s):
    best_n = [heapq.heappop(s) for _ in range(n)]
    k = np.random.randint(n)
    best = best_n[k]
    del best_n[k]
    for not_best in best_n:
        heapq.heappush(s,not_best)

    if best[2] != lib_version[best[1]]:
        continue
    if best[0]>=0:
        break
    schedule_time, n_books_shipped, lib_books = inp.libraries[best[1]]
    books = set(lib_books)-picked_books
    I.add(best[1])
    picked_books |= books
    changed = set()
    for book in books:
        for lid in libraries_per_book[book]:
            changed.add(lid)
    for lid in changed:
        lib_version[lid] +=1
        heapq.heappush(s, (-len(set(inp.libraries[lid][2])-picked_books),lid,lib_version[lid]))
    print(best[0],i, len(s),end="\r")
    i+=1
print()
print(len(I))
print(len(picked_books))


libraries_per_book =defaultdict(list)

for i in I:
    library = inp.libraries[i]
    for book in library[2]:
        libraries_per_book[book].append(i)

print(Counter([len(b) for b in libraries_per_book.values()]))

scores_per_unicity= defaultdict(list)

unique_books = set()
all_books = set()
for b, lib in libraries_per_book.items():
    if len(lib) == 1:
        unique_books.add(b)
    all_books.add(b)
    scores_per_unicity[len(lib)].append(inp.scores[b])
print(len(all_books),inp.B)
for unicity, scores in scores_per_unicity.items():
    print(unicity, np.mean(scores), np.std(scores), np.min(scores), np.max(scores))

library_map ={}
new_libraries = []

for i in I:
    library_map[len(new_libraries)] = i
    new_libraries.append(inp.libraries[i])

inp.libraries = new_libraries
picked_books = set()
picked_libraries = set()
time = 0
scheduled_libraries =[]


libraries_per_book =defaultdict(list)

for i, library in enumerate(inp.libraries):
    for book in library[2]:
        libraries_per_book[book].append(i)

book_counts = {i:len(lib[2]) for i, lib in enumerate(inp.libraries)}



def get_score(books):
    return sorted([(inp.scores[book],book) for book in books])[::-1]


def greedy_schedule(lid, time ,picked_books):
    schedule_time, n_books_shipped, lib_books = inp.libraries[lid]
    books = get_score(set(lib_books) - picked_books)
    t_left = max(0, inp.D - time - schedule_time)
    books_scanned = min(t_left * n_books_shipped, len(books))
    scheduled_books = [book[1] for book in books[:books_scanned]]
    picked_books |=  set(scheduled_books)
    scheduled_libraries.append((library_map[lid], scheduled_books))
    picked_libraries.add(lid)
    return time+schedule_time, scheduled_books, picked_books


lib_version = {l:0 for l in range(inp.L)}

def count_lib(lid):
    lib = inp.libraries[lid]
    new_books = set(lib[2])-picked_books
    cnt = len(new_books.intersection(unique_books))+0.5*len(new_books)
    if len(new_books.intersection(unique_books))<2 and False:
        cnt = len(new_books)
    return -cnt,lid, lib_version[lid]

s= [count_lib(lid) for lid in range(len(inp.libraries))]
heapq.heapify(s)
while(time <= inp.D and len(picked_libraries)< len(inp.libraries) and len(s)):
    print(time, inp.D, end="\r")
    best = heapq.heappop(s)
    if best[0] > 0:
        break
    if best[2] != lib_version[best[1]]:
        continue
    #print()
    #print(best[0])
    time, books, picked_books = greedy_schedule(best[1], time, picked_books)

    changed = set()
    for book in books:
        for lid in libraries_per_book[book]:
            changed.add(lid)
    for lid in changed:
        lib_version[lid] += 1
        heapq.heappush(s, count_lib(lid))

print()
inp = Input.from_argv()
sol = Solution(scheduled_libraries, inp)
print(sol.score(), inp.max_score())
sol.write()




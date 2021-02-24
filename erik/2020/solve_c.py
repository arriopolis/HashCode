from read_input import Input, Solution
from collections import defaultdict, Counter
import numpy as np
import heapq

inp = Input.from_argv()


# hypothesis: all books are instantly scanned
#for schedule_time, books_per_day, lib_books in inp.libraries:
#    assert books_per_day> len(lib_books)

# True

# metric bookscore/schedule_time


# check connectedness

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


# SOLUTION: metric bookscore/schedule_time
def run_greedy(seed):
    np.random.seed(seed)
    picked_books = set()
    picked_libraries = set()
    time = 0
    scheduled_libraries =[]
    max_len_bests = 1
    def get_score(books):
        return sorted([(inp.scores[book],book) for book in books])[::-1]

    def calc_pot_score_library(library, time):
        # schedule_time, n_books_shipped, [book_id]
        schedule_time, n_books_shipped, lib_books = library
        books = get_score(set(lib_books)- picked_books)
        t_left = max(0,inp.D-time-schedule_time)
        books_scanned = min(t_left*n_books_shipped, len(books))
        slack = t_left - np.ceil(books_scanned/n_books_shipped)
        return sum([book[0] for book in books[:books_scanned]])/schedule_time, slack

    def greedy_schedule(lid, time, picked_books):
        schedule_time, n_books_shipped, lib_books = inp.libraries[lid]
        books = get_score(set(lib_books) - picked_books)
        t_left = max(0, inp.D - time - schedule_time)
        books_scanned = min(t_left * n_books_shipped, len(books))
        scheduled_books = [book[1] for book in books[:books_scanned]]
        picked_books |=  set(scheduled_books)
        scheduled_libraries.append((lid, scheduled_books))
        picked_libraries.add(lid)
        return time+schedule_time, picked_books

    done = False
    while(time <= inp.D and len(picked_libraries)< len(inp.libraries)):
        print(time, inp.D,end ="\r")
        pot_scores = [(*calc_pot_score_library(library, time),i, library) if i not in picked_libraries else (-1,) for i,library in enumerate(inp.libraries)];
        pot_scores = sorted(pot_scores)[::-1]
        best = pot_scores[np.random.randint(3)]
        lid = best[2]
        time, picked_books = greedy_schedule(lid, time, picked_books)
    print()

    sol = Solution(scheduled_libraries, inp)
    print(sol.score(), inp.max_score())
    sol.write()

seed =0
while True:
    run_greedy(seed)
    seed +=1
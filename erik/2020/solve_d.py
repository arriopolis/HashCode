from read_input import Input, Solution
from collections import defaultdict
import numpy as np
import heapq


def run_greedy(seed):
    inp = Input.from_argv()
    inp.libraries = inp.libraries[1::2]
    np.random.seed(seed)
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
        scheduled_libraries.append((lid*2+1, scheduled_books))
        picked_libraries.add(lid)
        return time+schedule_time, scheduled_books, picked_books
    while(time <= inp.D and len(picked_libraries)< len(inp.libraries)):
        print(time, inp.D, end="\r")
        s = sorted([(count,i) for i, count in book_counts.items()])[::-1]
        time, books, picked_books = greedy_schedule(s[0][1], time, picked_books)
        for book in books:
            for lid in libraries_per_book[book]:
                book_counts[lid] -=1
    print()
    inp = Input.from_argv()
    sol = Solution(scheduled_libraries, inp)
    print(sol.score(), inp.max_score())
    sol.write()

seed =0
while True:
    run_greedy(seed)
    seed +=1
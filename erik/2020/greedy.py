from read_input import Input, Solution
import numpy as np

inp = Input.from_argv()

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
    return sum([book[0] for book in books[:books_scanned]]), slack

def greedy_schedule(lid, time):
    global picked_books, scheduled_libraries
    schedule_time, n_books_shipped, lib_books = inp.libraries[lid]
    books = get_score(set(lib_books) - picked_books)
    t_left = max(0, inp.D - time - schedule_time)
    books_scanned = min(t_left * n_books_shipped, len(books))
    scheduled_books = [book[1] for book in books[:books_scanned]]
    picked_books |=  set(scheduled_books)
    scheduled_libraries.append((lid, scheduled_books))
    picked_libraries.add(lid)
    return time+schedule_time

done = False
while(time <= inp.D and len(picked_libraries)< len(inp.libraries)):
    print(time, inp.D,end ="\r")
    pot_scores = [(*calc_pot_score_library(library, time),i, library) if i not in picked_libraries else (-1,) for i,library in enumerate(inp.libraries)];
    pot_scores = sorted(pot_scores)[::-1]
    bests = [pot_scores[0]]
    for pot_score in pot_scores:
        if pot_score[0] == -1:
            break
        scheduled_time = pot_score[3][0]
        if scheduled_time <bests[-1][1] and pot_score[1]< bests[-1][3][0]:
            bests.append(pot_score)
    if bests[0][0] <=0:
        break
    for best in bests[::-1][:max_len_bests]:
        lid = best[2]
        time = greedy_schedule(lid, time)
print()

sol = Solution(scheduled_libraries, inp)
print(sol.score(), inp.max_score())
sol.write()

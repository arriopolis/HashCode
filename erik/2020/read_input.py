import sys
from collections import deque

def read_input(file):
    return Input(file);


class Input:
    def __init__(self, file):
        self.file_name = file
        with open(file) as f:
            self.B, self.L, self.D = map(int, f.readline().split(' '))
            self.scores = list(map(int, f.readline().split(' ')))
            self.libraries = []
            for l in range(self.L):
                # schedule_time, n_books_shipped, [book_id]
                library = list(map(int, f.readline().split(' ')))[1:]
                library.append(list(map(int, f.readline().split(' '))))
                self.libraries.append(library)
    @staticmethod
    def from_argv():
        return Input(sys.argv[1])

    def max_score(self):
        return sum(self.scores)



class Solution:
    def __init__(self, libraries, input):
        assert isinstance(input, Input)
        self.input = input
        assert type(libraries) == list
        passed_libraries = set()
        for library in libraries:
            assert type(library) == tuple
            assert len(library) == 2
            assert type(library[0]) == int
            assert 0<=library[0]<input.L
            assert library[0] not in passed_libraries, "library scheduled twice"
            passed_libraries.add(library[0])
            assert type(library[1]) == list
            for book in library[1]:
                assert type(book) == int
                assert 0 <= book < input.B
                assert book in input.libraries[library[0]][2]
        self.libraries = libraries

    @staticmethod
    def from_file( file, input):
        libraries = []
        with open(file) as f:
            for i in range(int(f.readline())):
                id,_ =map(int, f.readline().split(' '))
                books = list(map(int, f.readline().split(' ')))
                libraries.append((id, books))
        return Solution(libraries, input)

    @staticmethod
    def from_argv(input =None):
        n_argv = 1
        if input is None:
            input = Input.from_argv()
            n_argv +=1
        return Solution.from_file(sys.argv[n_argv],input)

    def score(self):
        passed_books = set([])
        time =0
        active_libraries = []
        score =0
        def schedule(time, score):
            for n_books, books in active_libraries:
                for i in range(min(n_books*time, len(books))):
                    book = books.popleft()
                    if book not in passed_books:
                        passed_books.add(book)
                        score += self.input.scores[book]
                        #print(f"scanned book {book} added score {score}")

            return score

        for lid, books in self.libraries:
            schedule_time, books_shipped, lib_books = self.input.libraries[lid]
            schedule_time = min(schedule_time, self.input.D-time)
            score = schedule(schedule_time,score)
            time += schedule_time
            active_libraries.append((books_shipped, deque(books)))
            #print(f"added library {lid} to active libraries with books {books}")
            if time == self.input.D:
                return score
        score = schedule(self.input.D-time,score)
        return score

    def write(self):
        import os
        file_name = os.path.join("output",self.input.file_name.split("/")[-1][0]+"_"+str(self.score())+".out")
        with open(file_name, "w") as f:
            f.write(f"{len(self.libraries)}\n")
            for lid,books in self.libraries:
                f.write(f"{lid} {len(books)}\n")
                f.write(" ".join(map(str,books))+"\n")




if __name__ == "__main__":
    solution = Solution.from_argv()
    print(solution.score())
    solution.write()


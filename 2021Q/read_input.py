import sys

import collections

class Instance:
    def __init__(self, file):
        self.file_name = file
        with open(file as f):
            # parse input

    @staticmethod
    def rom_argv():
        return Instance(sys.argv[1])

    def score_upperbound(self):
        return float('inf')


class Solution:
    def __init__(self, solution, instance):
        assert isinstance(instance, Instance)
        self.instance = instance
        # typecheck the solution

    @staticmethod
    def from_file(file, instance):
        with open(file) as f:
            solution = None # parse solution from file
        return Solution(solution, instance)


    @staticmethod
    def from_argv(instance = None):
        n_argv = 1
        if instance is None:
            instance = Instance.from_argv()
            n_argv += 1
        return Solution.from_file(sys.argv[n_argv], instance)

    def score(self):
        # calculate score
        score = 0
        return score

    def write(self):
        import os
        file_name = f"{self.instance.file_name.split('/')[-1][0]}_{self.score()}.out"
        file_path = os.path.join("output",
                                 file_name)

        with open(file_path, "w") as f:
            pass
            # write this to file
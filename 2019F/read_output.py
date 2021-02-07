import sys
from read_input import Instance


class Solution:
    def __init__(self, filepath):
        self.ready_time_of_file_at_server = []

        f = open(filepath, 'r')
        self.E = int(f.readline())
        self.compilation_steps = []
        for _ in range(self.E):
            name, s = f.readline().split()
            self.compilation_steps.append((name, int(s)))

    # def determine_score(self, instance):
    #     self.ready_time_of_file_at_server = [[[] for file in range(instance.C)] for server in range(S)]
    #     server_time = [0 for server in range(S)]
    #     for step in self.compilation_steps:
    #         name, server = step[0], step[1]
    #         _, c, r = [file for file in instance.compiled_files][0]
    #         server_time[server] += c
    #         self.ready_time_of_file_at_server[server][] =

def main():
    solution = Solution(sys.argv[1])
    print(solution.E)
    for e in range(solution.E):
        print(solution.compilation_steps[e])


if __name__ == '__main__':
    main()
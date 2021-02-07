import sys


class Solution:
    def __init__(self, filepath):
        f = open(filepath, 'r')
        self.E = int(f.readline())
        self.compilation_steps = []
        for _ in range(self.E):
            name, s = f.readline().split()
            self.compilation_steps.append((name, int(s)))


def main():
    solution = Solution(sys.argv[1])
    print(solution.E)
    for e in range(solution.E):
        print(solution.compilation_steps[e])


if __name__ == '__main__':
    main()
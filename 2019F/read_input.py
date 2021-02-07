import sys

class Instance:
    def __init__(self, filepath):
        f = open(filepath, 'r')
        self.C, self.T, self.S = map(int, f.readline().split())
        self.compiled_files = []
        self.dependencies = []
        self.target_files = []
        for _ in range(self.C):
            name, c, r = f.readline().split()
            self.compiled_files.append((name, int(c), int(r)))
            line = f.readline().split()
            self.dependencies = [[] for i in range(self.C)]
            if len(line):
                self.dependencies[_].append(line[1:])
        for _ in range(self.T):
            name, d, g = f.readline().split()
            self.target_files.append((name, d, g))


def main():
    instance = Instance(sys.argv[1])
    print(instance.C, instance.T, instance.S)
    for index in range(instance.C):
        print(instance.compiled_files[index])
        print(instance.dependencies[index])
    print(instance.target_files)

if __name__ == '__main__':
    main()
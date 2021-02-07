import sys


class Instance:
    def __init__(self, filepath):
        f = open(filepath, 'r')
        self.C, self.T, self.S = map(int, f.readline().split())
        self.compiled_files = []
        self.compiled_files_dict = dict()
        self.dependencies = []
        self.dependencies_dict = dict()
        self.target_files = []
        self.target_files_dict = dict()
        for _ in range(self.C):
            name, c, r = f.readline().split()
            self.compiled_files.append((name, int(c), int(r)))
            self.compiled_files_dict[name] = (int(c), int(r))
            line = f.readline().split()
            self.dependencies.append(tuple(line[1:]))
            self.dependencies_dict[name] = tuple(line[1:])
        for _ in range(self.T):
            name, d, g = f.readline().split()
            self.target_files.append((name, d, g))
            self.target_files_dict[name] = (d, g)


def main():
    instance = Instance(sys.argv[1])
    print(instance.C, instance.T, instance.S)
    for index in range(instance.C):
        print(instance.compiled_files[index])
        print(instance.dependencies[index])
    for index in range(instance.T):
        print(instance.target_files[index])


if __name__ == '__main__':
    main()
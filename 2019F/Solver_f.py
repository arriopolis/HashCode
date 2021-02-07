if __name__ == '__main__':
    import sys
    from read_input import Instance
    from read_output import Solution

    instance = Instance(sys.argv[1])

    dict_depth = {}
    solution = []

    min_replication_time = 10000000000000
    count = 0
    N = 0
    for file, deadline, points in instance.target_files:

        min_time = 1000000000000
        N_add = 0
        for dep in instance.dependencies_dict[file]:
            N_add += 1
            min_time = min(min_time, instance.compiled_files_dict[dep][1])
            min_replication_time = min(min_replication_time, instance.compiled_files_dict[dep][1])
        if deadline >= 100 + instance.compiled_files_dict[file][0]:
            solution.append(file)
            print('---', file, '---')
            print('Minimum compilation time:', '100 +', instance.compiled_files_dict[file][0], '(file) =', 100 + instance.compiled_files_dict[file][0])
            print('Minimum replication time:', min_time)
            print('Deadline:', deadline)
            count += 1
            N += N_add + 1

    print()
    print('Minimum replication time:', min_replication_time)
    print()
    print('Amount feasible:', count)

    f = open('res/f.txt', 'w')
    count = 0
    f.write(str(N) + '\n')
    for file in solution:
        for dep in instance.dependencies_dict[file]:
            f.write(dep + ' ' + str(count) + '\n')
        f.write(file + ' ' + str(count) + '\n')
        count += 1

    f.close()






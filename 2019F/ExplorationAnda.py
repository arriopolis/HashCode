if __name__ == '__main__':
    import sys
    from read_input import Instance
    import matplotlib.pyplot as plt

    instance = Instance(sys.argv[1])

    dict_depth = {}

    for i, x in enumerate(instance.compiled_files):
        # print(x[0], instance.dependencies_dict[x[0]])
        if instance.dependencies_dict[x[0]] == ():
            dict_depth[x[0]] = 0
        else:
            max_depth = 0
            for dep in instance.dependencies_dict[x[0]]:
                max_depth = max(max_depth, dict_depth[dep])
            dict_depth[x[0]] = max_depth + 1

    print(max(dict_depth.values()))
    plt.hist(dict_depth.values())
    plt.show()





from read_input import Instance, Solution
import matplotlib.pyplot as plt

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Supply the correct command line arguments.")
        sys.exit()
    instance = Instance.from_argv()

    times = []
    for i,path in enumerate(instance.paths):
        time = 0
        for street in path[1:]:
            time += instance.streets[street][2]

        times.append(time/instance.D)

        instance.paths[i] = [time] + instance.paths[i]

    instance.paths.sort(reverse = True)
    # print(instance.paths)

    solution = []
    for path in instance.paths:
    # path = instance.paths[0]
        for street in path[1:]:
            print(street, instance.streets[street][1])
            solution.append((instance.streets[street][1], [(street, 1)]))
            # for intersection in range(instance.I):

    s = Solution(solution, instance)
    s.write()



    # plt.hist(times)
    # plt.show()
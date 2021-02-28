from read_input import Instance, Solution
# import matplotlib.pyplot as plt
import queue


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Supply the correct command line arguments.")
        sys.exit()
    instance = Instance.from_argv()

    incoming_streets = [[] for _ in range(instance.I)]
    for street in instance.streets:
        incoming_streets[instance.streets[street][1]].append(street)

    print('Incoming streets calculated')

    green_needed = []
    for isct in range(instance.I):
        dict_temp = {}
        for street in incoming_streets[isct]:
            dict_temp[street] = [0]*instance.D
        green_needed.append(dict_temp)

    print('Initialisation complete')

    count = 0
    for path in instance.paths:
        count += 1
        print('Progress:', count / instance.V * 100, '%                    ', end='\r')

        time = 0
        isct = instance.streets[path[0]][1]
        green_needed[isct][path[0]][time] += 1
        for street in path[1:-1]:
            time += instance.streets[street][2]
            isct = instance.streets[street][1]
            green_needed[isct][street][time] += 1

    isct = 1
    for street in incoming_streets[isct]:
        plt.plot(range(instance.D), green_needed[isct][street])
    plt.show()

    isct = 2
    for street in incoming_streets[isct]:
        plt.plot(range(instance.D), green_needed[isct][street])
    plt.show()

    isct = 44
    for street in incoming_streets[isct]:
        plt.plot(range(instance.D), green_needed[isct][street])
    plt.show()

    # solution = []
    # for path in instance.paths:
    #     time = 0
    #     for street in path[1:]:
    #         time += instance.streets[street][2]
    #         solution.append((instance.streets[street][1], [(street, 1)]))
    #         # for intersection in range(instance.I):
    #
    # s = Solution(solution, instance)
    # # s.write()
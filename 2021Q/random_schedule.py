from read_input import *
import random

def random_solution():
    import sys
    import os
    while True:
        for file in os.listdir('input'):
            instance = Instance('input/' + file)
            # if file in ['a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt', 'f.txt']:
            if file in ['a.txt', 'b.txt']:
                continue
            intersections = [[street for street in instance.streets if instance.streets[street][1] == intersection] for
                             intersection in range(instance.I)]
            lights = [[] for _ in intersections]
            for index, intersection in enumerate(intersections):
                schedule = []
                for street in random.sample(intersection, len(intersection)):
                    min_green_time = random.randint(1, min(1, instance.D // 2))
                    max_green_time = random.randint(min_green_time, min(2, instance.D - 1))
                    schedule.append((street, random.randint(min_green_time, max_green_time)))
                lights[index] = (index, schedule)
            solution = Solution(lights, instance)
            solution.write()


def main():
    import multiprocessing
    max_num_of_procs = 10
    for proc in range(max_num_of_procs):
        multiprocessing.Process(target=random_solution, args=()).start()


if __name__ == "__main__":
        main()
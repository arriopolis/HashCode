from read_input import read_input
from read_solution import *
import random

if __name__ == "__main__":
    import sys
    solution = Solution(sys.argv[1])

    x, y = 0, 0
    check = True
    while check:
        random_building = random.choice(solution.buildings)
        solution.add_building_plan_to_grid(random_building[0], random_building[4], x, y)
        check = False
        solution.print()


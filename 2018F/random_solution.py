from read_input import read_input
from read_solution import *
import random

if __name__ == "__main__":
    import sys
    counter = 0
    best_score = 0
    best_solution = []

    while counter < pow(10,3):
        solution = Solution(sys.argv[1])
        y, x = 0, 0
        check = True
        outer_tries = 0
        building_counter = 0
        while check and outer_tries < pow(10,3):
            width_building = []
            height_builing = []
            random_building = []
            infeasible = True
            inner_tries = 0
            if random.randint(0, 100) < 20:
                x += 1
            while infeasible and inner_tries < 10:
                random_building = random.choice(solution.buildings)
                width_building = len(random_building[4][0])
                height_builing = len(random_building[4])
                if x + width_building < solution.w and y + height_builing < solution.r and not solution.would_building_overlap_when_added_to_grid(random_building[0], random_building[4], y, x):
                    infeasible = False
                inner_tries+=1
            if not infeasible:
                solution.constructed_buildings.append((building_counter, y, x))
                solution.add_building_plan_to_grid(random_building[0], random_building[4], y, x)
                x += width_building
                building_counter+=1
            else:
                x = 0
                y += 1
            outer_tries+=1
        counter+=1
        score = solution.determine_score()
        print(score)
        if score > best_score:
            best_score = score
            best_solution = solution
        solution.print()
    print(best_solution.determine_score())
    best_solution.print()



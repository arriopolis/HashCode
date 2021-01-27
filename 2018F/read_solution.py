from read_input import read_input
from copy import deepcopy
import sys

class Solution:
    def __init__(self, input_file):
        self.r, self.w, self.D, self.B, self.residentials, self.utilities = read_input(input_file)
        self.buildings = self.residentials + self.utilities
        self.building_coordinates = []
        self.constructed_buildings = []
        self.N = []
        self.grid = [['.' for x in range(self.w)] for y in range(self.r)]

    def read_solution(self, output_file):
        f = open(output_file, "r")
        self.N = int(f.readline().strip())
        count = 0
        for line in f.read().split("\n"):
            id, row, column = map(int, line.split(" "))
            self.constructed_buildings.append((id, row, column))
            building_plan = self.get_building_plan_by_id(id)
            self.add_building_plan_to_grid(count, building_plan, row, column)
            count+=1

    def get_building_plan_by_id(self, id):
        building = [building_plan for building_plan in self.buildings if building_plan[0]==id][0]
        building_plan = building[4]
        return building_plan

    def build_coordinates(self):
        self.building_coordinates = []
        for building in self.constructed_buildings:
            building_coordinates = []
            building_plan = self.buildings[building[0]][4]
            r = building[1]
            w = building[2]
            for y in range(len(building_plan)):
                for x in range(len(building_plan[0])):
                    if building_plan[y][x]:
                        self.grid[r + y][w + x] = building[0]
                        building_coordinates += [[r + y, w + x]]
            self.building_coordinates += [building_coordinates]

    def add_building_plan_to_grid(self, index, building_plan, r, w):
        for y in range(len(building_plan)):
            for x in range(len(building_plan[0])):
                if building_plan[y][x]:
                    if self.grid[r + y][w + x] != '.':
                        sys.exit("OVERLAP")
                    self.grid[r + y][w + x] = index

    def would_building_overlap_when_added_to_grid(self, index, building_plan, r, w):
        for y in range(len(building_plan)):
            for x in range(len(building_plan[0])):
                if building_plan[y][x]:
                    if self.grid[r + y][w + x] != '.':
                        return True
        return False

    def check_borders(self):
        top = self.grid[0]
        if not self.check_border(top):
            return False
        bottom = self.grid[-1]
        if not self.check_border(bottom):
            return False
        left = [row[0] for row in self.grid]
        if not self.check_border(left):
            return False
        right = [row[-1] for row in self.grid]
        if not self.check_border(right):
            return False
        return True

    def check_border(self, border):
        return len([value for value in border if value != "."]) > 0



    def print(self):
        for line in self.grid:
            print(''.join([str(value) for value in line]))

    @staticmethod
    def print_grid(grid):
        for line in grid:
            print([str(value) for value in line])

    # def grid_with_only_constructed_buildings(self, first_id, second_id):
    #     adjusted_grid = deepcopy(self.grid)
    #     for ir, row in enumerate(adjusted_grid):
    #         for iv, value in enumerate(row):
    #             if value == first_id + 1:
    #                 adjusted_grid[ir][iv] = 1
    #             elif value == second_id + 1:
    #                 adjusted_grid[ir][iv] = 2
    #             else:
    #                 adjusted_grid[ir][iv] = 0
    #     return adjusted_grid

    def distance_between_two_buildings(self, first_id, second_id):
        best_distance = pow(10,6)
        for first_coordinate in self.building_coordinates[first_id - 1]:
            for second_coordinate in self.building_coordinates[second_id - 1]:
                distance = abs(first_coordinate[0] - second_coordinate[0]) + abs(first_coordinate[1] - second_coordinate[1])
                if distance < best_distance:
                    best_distance = distance
        return best_distance

    def determine_score(self):
        self.build_coordinates()
        residential_buildings = [building for building in self.constructed_buildings if building[0] in [residential[0] for residential in self.residentials]]
        utility_buildings = [building for building in self.constructed_buildings if building[0] in [residential[0] for residential in self.utilities]]
        residential_buildings_indices = [ib for ib, building in enumerate(self.constructed_buildings) if building[0] in [residential[0] for residential in self.residentials]]
        utility_buildings_indices = [ib for ib, building in enumerate(self.constructed_buildings) if building[0] in [residential[0] for residential in self.utilities]]
        number_of_utility_types = max([utility[3] for utility in self.utilities]) + 1
        score = 0
        for ir, residential in enumerate(residential_buildings):
            utility_score = [0 for _ in range(number_of_utility_types)]
            for iu, utility in enumerate(utility_buildings):
                distance = self.distance_between_two_buildings(residential_buildings_indices[ir] + 1, utility_buildings_indices[iu] + 1)
                if distance <= self.D:
                    utility_score[self.buildings[utility[0]][3]] = self.buildings[residential[0]][3]
            score += sum(utility_score)
        return score

        # number_of_utility_types = max([utility[3] for utility in self.utilities]) + 1
        # distance_from_residential_building_to_utility = [[0 for _ in range(number_of_utility_types)] for building in residential_building_indices]
        # for i, constructed_residential_index in enumerate(residential_building_indices):
        #     capacity = self.buildings[self.constructed_buildings[constructed_residential_index][0]][3]
        #     for constructed_utility_index in utility_building_indices:
        #         utility_building_plan = self.buildings[self.constructed_buildings[constructed_utility_index][0]]
        #         distance = self.distance_between_two_buildings(constructed_residential_index + 1, constructed_utility_index + 1)
        #         if distance <= self.D:
        #             if distance_from_residential_building_to_utility[i][utility_building_plan[3]] == 0 or distance < distance_from_residential_building_to_utility[i][utility_building_plan[3]]:
        #                 distance_from_residential_building_to_utility[i][constructed_utility_index] = capacity
        # return sum([sum(row) for row in distance_from_residential_building_to_utility])

if __name__ == '__main__':
    solution = Solution(sys.argv[1])
    solution.read_solution(sys.argv[2])
    print(solution.determine_score())

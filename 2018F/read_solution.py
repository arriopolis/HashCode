from read_input import read_input
from copy import deepcopy
import sys

class Solution:
    def __init__(self, input_file):
        self.r, self.w, self.D, self.B, self.residentials, self.utilities = read_input(input_file)
        self.buildings = self.residentials + self.utilities
        self.N, self.grid = [], []

    def read_solution(self, output_file):
        f = open(output_file, "r")
        self.N = int(f.readline().strip())
        self.grid = [["." for x in range(self.w)] for y in range(self.r)]
        count = 1
        for line in f.read().split("\n"):
            id, row, column = map(int, line.split(" "))
            building_plan = self.get_building_plan_by_id(id)
            self.add_building_plan_to_grid(count, building_plan, row, column)
            count+=1

    def get_building_plan_by_id(self, id):
        building = [building_plan for building_plan in self.buildings if building_plan[0]==id][0]
        building_plan = building[4]
        return building_plan

    def add_building_plan_to_grid(self, index, building_plan, r, w):
        for y in range(len(building_plan)):
            for x in range(len(building_plan[0])):
                if building_plan[y][x]:
                    self.grid[r + y][w + x] = str(index)

    def print(self):
        for line in self.grid:
            print(line)

if __name__ == '__main__':
    solution = Solution(sys.argv[1])
    solution.read_solution(sys.argv[2])
    solution.print()

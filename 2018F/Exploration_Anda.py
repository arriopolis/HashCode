class CityPlanner:

    def __init__(self, h, w, d, b, residentials, services):
        self.city_plan = [[-1 for _ in range(w)] for _ in range(h)]
        self.building_list = []
        self.city_height = h
        self.city_width = w
        self.walking_distance = d
        self.residential_buildings = residentials
        self.utility_buildings = services
        self.add_building_to_plan(self.sort_by_highest_capacity()[0], (0, 0))

    def add_building_to_plan(self, building, location):
        self.building_list.append((building[0], location[0], location[1]))
        building_id, building_height, building_width, cp, layout = building
        for i in range(location[0], location[0]+building_height):
            for j in range(location[1], location[1]+building_width):
                self.city_plan[i][j] = building_id

        print("added", building[0:4], "to city plan at location", location)

    def find_empty_spot(self):
        for i in range(self.city_height-50):
            for j in range(self.city_width-50):
                if self.city_plan[i][j] == -1:
                    return (i, j)

    def determine_best_residential(self, location):
        best_score = 0
        best_building = -1
        for residential in self.residential_buildings:
            near_building_indices = set()

            for i in range(max(location[0]-self.walking_distance,0), location[0]+self.walking_distance+residential[1]):
                for j in range(max(location[1] - self.walking_distance, 0), location[1] + self.walking_distance + residential[2]):
                    near_building_indices.add(self.city_plan[i][j])

            score = 0
            for utility in self.utility_buildings:
                if utility[0] in near_building_indices:
                    score += residential[3]

            if score > best_score:
                best_score = score
                best_building = residential

        return best_building, best_score

    def determine_best_utility(self, location):
        best_score = 0
        best_building = -1
        for utility in self.utility_buildings:
            near_building_indices = set()

            for i in range(max(location[0] - self.walking_distance, 0),
                           location[0] + self.walking_distance + utility[1]):
                for j in range(max(location[1] - self.walking_distance, 0),
                               location[1] + self.walking_distance + utility[2]):
                    near_building_indices.add(self.city_plan[i][j])

            score = 0
            for residential in self.residential_buildings:
                if residential[0] in near_building_indices:
                    score += residential[3]

            if score > best_score:
                best_score = score
                best_building = utility

        return best_building, best_score

    def sort_by_highest_capacity(self):
        sorted_residentials = sorted(self.residential_buildings, key=lambda x: x[3], reverse=True)

        return sorted_residentials

    def add_best_buildings_to_plan(self):
        score_residential = -1
        score_utility = -1

        while score_residential != 0 or score_utility != 0:
            location = self.find_empty_spot()
            best_residential, score_residential = self.determine_best_residential(location)
            best_utility, score_utility = self.determine_best_utility(location)

            if score_utility > score_residential:
                self.add_building_to_plan(best_utility, location)
            else:
                self.add_building_to_plan(best_residential, location)


def print_building_layout(block):
    for row in block:
        for x in row:
            if x:
                print('#', end='')
            else:
                print('.', end='')
        print('\n', end='')

if __name__ == '__main__':
    import sys
    from read_input import read_input,reduce_same_layouts
    from read_solution import Solution

    h, w, d, b, residentials, services = read_input(sys.argv[1])
    city_planner = CityPlanner(h, w, d, b, residentials, services)
    city_planner.add_best_buildings_to_plan()
    print(city_planner.building_list)


    # solution = Solution(sys.argv[1])
    # solution.read_solution(sys.argv[2])
    # print(solution.determine_score())



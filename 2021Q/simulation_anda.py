import sys
# from collections import deque, defaultdict


class Instance:
    def __init__(self, file):
        self.file_name = file
        with open(file) as f:
            self.D, self.I, self.S, self.V, self.F = map(int, next(f).strip().split())
            self.streets = {}
            for _ in range(self.S):
                B, E, name, L = next(f).strip().split()
                self.streets[name] = (int(B), int(E), int(L))
            self.paths = []
            for _ in range(self.V):
                p = list(next(f).strip().split())[1:]
                self.paths.append(p)

    @staticmethod
    def from_argv():
        return Instance(sys.argv[1])

    def score_upperbound(self):
        return self.V * (self.F + self.D)


class Solution:
    def __init__(self, solution, instance):
        assert isinstance(instance, Instance)
        self.instance = instance

        allowed_streets = set(instance.streets.keys())
        assert type(solution) == list
        found_intersections = set()
        for intersection in solution:
            assert type(intersection) == tuple
            assert len(intersection) == 2
            iid, streets = intersection
            assert type(iid) == int
            assert iid not in found_intersections
            found_intersections.add(iid)
            assert 0 <= iid < instance.I
            assert type(streets) == list
            found_streets = set()
            for street in streets:
                assert len(street) == 2
                sn, time = street
                assert sn in allowed_streets
                assert type(sn) == str
                assert sn not in found_streets
                assert type(time) == int
                assert 1 <= time <= instance.D
                found_streets.add(sn)

        self.solution = solution

    @staticmethod
    def from_file(file, instance):
        with open(file) as f:
            solution = list()  # parse solution from file

            for _ in range(int(f.readline())):
                iid = int(f.readline())
                streets = []
                for _ in range(int(f.readline())):
                    sn, time = f.readline().split(" ")
                    streets.append((sn, int(time)))
                solution.append((iid, streets))
        return Solution(solution, instance)

    @staticmethod
    def from_argv(instance = None):
        n_argv = 1
        if instance is None:
            instance = Instance.from_argv()
            n_argv += 1
        return Solution.from_file(sys.argv[n_argv], instance)

    def score(self):
        from timeit import default_timer as timer
        start_time = timer()
        streets = self.instance.streets
        score = 0

        active_intersections = set()
        for path in self.instance.paths:
            for street in path[0:-1]:
                active_intersections.add(self.instance.streets[street][1])

        intersections = {}
        for intersection in self.solution:
            isct = intersection[0]
            if isct in active_intersections:
                queues = {}
                schedule = {}
                for i, (street, time) in enumerate(intersection[1]):
                    queues[street] = 0
                    schedule[street] = (time, intersection[1][(i+1)%len(intersection[1])][0])
                intersections[isct] = [intersection[1][0][0], intersection[1][0][1], queues, schedule]

        cars = {}
        for i, path in enumerate(self.instance.paths):
            street = path[0]
            isct = streets[street][1]
            place_in_queue = intersections[isct][2][street]
            cars[i] = [0, place_in_queue, 0, path]
            intersections[isct][2][street] += 1

        # print('cars:')
        # print(cars)
        # print('intersections:')
        # print(intersections)

        active_cars = set(cars.keys())
        for t in range(self.instance.D):
            print('Progress: %.1f %%' %(t / self.instance.D * 100), end='\r')
            # print()
            # print('Iteration: ', t)
            # print('cars:', cars)
            remove_cars = set()
            for car in cars:
                # print('car', car, ':', cars[car])

                [idx_on_path, place_in_queue, progress_on_road, path] = cars[car]
                street = path[idx_on_path]
                isct = streets[street][1]

                if progress_on_road == 0:
                    if street == intersections[isct][0]:  # light is green
                        # move up one element in the queue
                        if place_in_queue > 0:
                            place_in_queue -= 1
                            cars[car] = [idx_on_path, place_in_queue, progress_on_road, path]
                            continue

                        # cross intersection and reduce queue size
                        else:  # place_in_queue == 0
                            idx_on_path += 1
                            progress_on_road = streets[street][2] - 1
                            intersections[isct][2][street] = max(0, intersections[isct][2][street] - 1)
                            cars[car] = [idx_on_path, place_in_queue, progress_on_road, path]
                            continue

                # move along street and enter queue or remove from road
                else:
                    progress_on_road -= 1
                    if progress_on_road == 0:
                        if idx_on_path == len(path) - 1:  # car reached end of route
                            remove_cars.add(car)
                            continue
                        place_in_queue = intersections[isct][2][street]
                        intersections[isct][2][street] += 1
                    cars[car] = [idx_on_path, place_in_queue, progress_on_road, path]
                    continue

            for car in remove_cars:
                score += self.instance.F + (self.instance.D - t - 1)
                del cars[car]

            for isct in intersections:
                [green_street, time_green, queues, schedule] = intersections[isct]
                time_green -= 1
                if time_green == 0:
                    (time_green, green_street) = schedule[green_street]
                intersections[isct] = [green_street, time_green, queues, schedule]

        print('Time elapsed: %.2f seconds' %(timer()-start_time))
        return score

    def write(self):
        import os
        score = self.score()
        print(f"New score is {score} which is {score/self.instance.score_upperbound()*100}% of upperbound.")
        file_name = f"{os.path.split(self.instance.file_name)[-1][0]}_{score}.out"
        file_path = os.path.join("output", file_name)

        with open(file_path, "w") as f:
            f.write(f"{len(self.solution)}\n")
            for iid, streets in self.solution:
                f.write(f"{iid}\n")
                f.write(f"{len(streets)}\n")
                for sn, time in streets:
                    f.write(f"{sn} {time}\n")


if __name__ == "__main__":
    print(Solution.from_argv().score())

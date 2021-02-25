import sys

class Instance:
    def __init__(self, file):
        self.file_name = file
        with open(file) as f:
            self.D, self.I, self.S, self.V, self.F = map(int,next(f).strip().split())
            self.streets = {}
            for _ in range(self.S):
                B,E,name,L = next(f).strip().split()
                self.streets[name] = (int(B),int(E),int(L))
            self.paths = []
            for _ in range(self.V):
                p = list(next(f).strip().split())[1:]
                self.paths.append(p)

    @staticmethod
    def from_argv():
        return Instance(sys.argv[1])

    def score_upperbound(self):
        return self.V * (self.F + self.D)


from collections import deque, defaultdict

class Solution:
    def __init__(self, solution, instance):
        assert isinstance(instance, Instance)
        self.instance = instance
        # typecheck the solution

        # solution = list(
        #   (intersection_id, list((street, time),....),
        #   (inte...)
        #   )
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
            assert 0<= iid < instance.I
            assert type(streets) == list
            found_streets = set()
            for street in streets:
                assert len(street) == 2
                sn, time = street
                assert sn in allowed_streets
                assert type(sn) == str
                assert sn not in found_streets
                assert type(time) == int
                assert 1<= time<= instance.D
                found_streets.add(sn)

        self.solution = solution


    @staticmethod
    def from_file(file, instance):
        with open(file) as f:
            solution = list() # parse solution from file\

            for _ in range(int(f.readline())):
                iid = int(f.readline())
                streets =[]
                for _ in range(int(f.readline())):
                    sn, time = f.readline().split(" ")
                    streets.append((sn,int(time)))
                solution.append((iid, streets))
        return Solution(solution, instance)


    @staticmethod
    def from_argv(instance = None):
        n_argv = 1
        if instance is None:
            instance = Instance.from_argv()
            n_argv += 1
        return Solution.from_file(sys.argv[n_argv], instance)

    def score(self, show_streets= False):
        # calculate score
        score = 0
        cars_tl = {s:deque() for s in self.instance.streets.keys()}
        cars_in_transit = []
        schedules = {iid: streets for iid, streets in self.solution}
        current_tl = {iid: (0,streets[0][1]+1) for iid, streets in self.solution}

        vehicles_left_on_street = defaultdict(int)
        ineffective_tl = defaultdict(int)

        for i, path in enumerate(self.instance.paths):
            cars_tl[path[0]].append(i)




        for t in range(self.instance.D):
            # print(f"---{t}----")
            # print(cars_in_transit)
            new_cars_in_transit =[]
            active_streets = []
            #calculate active streets
            for iid, (idx, time_left) in current_tl.items():
                active_streets.append(schedules[iid][idx][0])
                time_left -=1
                if time_left == 0:
                    if show_streets and len(cars_tl[schedules[iid][idx][0]]) >0 :
                        vehicles_left_on_street[schedules[iid][idx][0]]=max(len(cars_tl[schedules[iid][idx][0]]),vehicles_left_on_street[schedules[iid][idx][0]])
                    idx = (idx+1) % len(schedules[iid])
                    time_left = schedules[iid][idx][1]
                current_tl[iid] = (idx, time_left)
            #     if iid == 0:
            #         print(schedules[iid][idx][0], time_left, t)
            # print(active_streets)


            # cars pass active_streets
            for sn in active_streets:
                cars = cars_tl[sn]
                if len(cars)>0:
                    car = cars.popleft()
                    idx = self.instance.paths[car].index(sn)+1
                    next_street = self.instance.paths[car][idx]
                    new_cars_in_transit.append((car, next_street, self.instance.streets[next_street][2]-1))
                else:
                    ineffective_tl[sn] += 1

            for car, street, time_left in cars_in_transit:
                time_left -= 1
                if time_left > 0:
                    new_cars_in_transit.append((car,street,time_left))
                else:
                    if street == self.instance.paths[car][-1]:
                        #calculate score
                        # print(f"{car} is binnen")
                        score += self.instance.F + self.instance.D - t
                    else:
                        cars_tl[street].append(car)
            cars_in_transit = new_cars_in_transit
        if show_streets:
            print("vehicles_left on street:")
            for key, n in sorted(vehicles_left_on_street.items(), key = lambda x:-x[1])[:10]:
                if n > 2:
                    print(key,n)

            print("ineffective streets:")
            for key, n in sorted(ineffective_tl.items(), key = lambda x:-x[1])[:10]:
                print(key,n)
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
            # write this to file


if __name__ == "__main__":
    print(Solution.from_argv().score(True))

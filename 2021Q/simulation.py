


from collections import deque, defaultdict
def simulate(solution):
    def print(*args):
        pass
    score = 0

    # set initial condition
    intersections = {}
    intersection_change_at_t = defaultdict(deque)
    active_street_lights = dict()
    for iid, streets in solution.solution:
        if len(streets)>0:
            if len(streets)>1:
                intersections[iid] = [0, streets]
                intersection_change_at_t[streets[0][1]].append(iid)
            active_street_lights[iid] = streets[0][0]



    traffic_light_queues = defaultdict(deque)
    paths = [ deque(path[::-1]) for path in solution.instance.paths]
    for car, path in enumerate(paths):
        street = path.pop()
        traffic_light_queues[street].appendleft(car)
        if path:
            del paths[car]

    cars_at_intersection_at_t = defaultdict(deque)

    time_waited = defaultdict(int)


    # START SIMULATION
    for t in range(solution.instance.D):
        print(f"----{t}----")
        # handle traffic light switching
        for iid in intersection_change_at_t[t]:
            idx, streets = intersections[iid]
            idx = (idx + 1) %len(streets)
            intersection_change_at_t[t+streets[idx][1]].append(iid)
            active_street_lights[iid] = streets[idx][0]
            intersections[iid][0] = idx
            print(f"Changing {iid} to {streets[idx][0]}")

        # handle riding cars reaching end of road
        for car, street in cars_at_intersection_at_t[t]:
            print(f"{car} found at end of {street}")
            if paths[car]:
                traffic_light_queues[street].appendleft(car)
            else:
                print(f"writing score for {car}")
                # calculate_score
                score += solution.instance.F + (solution.instance.D-t)


        # Handle cars at traffic lights
        for street in list(active_street_lights.values()):
            queue = traffic_light_queues[street]
            if queue:
                car = queue.pop()
                path = paths[car]
                nstreet = path.pop()
                cars_at_intersection_at_t[t+solution.instance.streets[nstreet][2]].append((car,nstreet))
                print(f"letting {car} pass at {street} going to {nstreet}")

        del intersection_change_at_t[t]
        del cars_at_intersection_at_t[t]

        # for street, queue in traffic_light_queues.items():
        #     time_waited[street] += len(queue)

    return score#, time_waited

import heapq
def simulate2(sol):
    def print(*args):
        pass
    #Car centric
    class Car:
        def __init__(self, path, instance, tls, id):
            self.id = id
            self.instance = instance
            self.path = deque()
            self.init_path(path, tls, instance)
            self.feasible = True
            self.score = 0
            self.streets = list(path)

        def init_path(self, path, tls, instance):
            for street in path[:-1]:
                if street not in tls:
                    print(f"Car {self.id} is not feasible since {street} is not scheduled")
                    self.feasible = False
                    return
                self.path.extend([instance.streets[street][2], tls[street]])
            self.path.append(instance.streets[path[-1]][2])
            self.path.popleft()

        def __str__(self):
            res = f"Car({self.id})"
            if not self.feasible:
                return res+"<INFEASIBLE>"
            return res+f"<{'|'.join(map(str,self.path))}>"

        def step(self, t):
            # Car is done
            if not self.path:
                if self.feasible:
                    self.score = self.instance.F + (self.instance.D-t)
                    print(f"Car {self.id} finished at {t} with score {self.score}")
                return self.instance.D+100

            objective = self.path.popleft()
            if type(objective) == int:
                print(f"{t}: Car {self.id} passes intersection {self.streets[0]},{self.streets[1]}")
                self.streets = self.streets[1:]
                next_t =  t+objective
            else:
                # Objective is a trafficlight
                print(f"{t}: Car {self.id} reaches end of {self.streets[0]}")
                next_t =  objective.arrive(t)
            if next_t == t:
                return self.step(next_t)
            return next_t



    class TrafficLight:
        def __init__(self, start_time, time_active, period, street):
            self.period = period
            self.end_time = start_time + time_active
            self.start_time = start_time
            self.street = street
            self.last_car_t = -1

        def __str__(self):
            return f"TrafficLight<{self.street}>"

        def next_valid_t(self, t):
            t_in_period = t%self.period
            t_to_period = (t//self.period)*self.period
            if t_in_period < self.start_time:
                return t_to_period+self.start_time
            if t_in_period >= self.end_time:
                return t_to_period+self.period+self.start_time
            else:
                return t

        def arrive(self, t):
            next_t = self.next_valid_t(max(self.last_car_t+1, t))
            self.last_car_t = next_t
            return next_t


    # SETUP initial conditions
    traffic_lights = dict()
    for iid, schedule in sol.solution:
        period = sum([ time for _, time in schedule])
        start_time = 0
        for street, time in schedule:
            traffic_lights[street] = TrafficLight(start_time, time, period, street)
            start_time += time
        assert start_time == period
    cars =[]
    for id, path in enumerate(sol.instance.paths):
        cars.append(Car(path, sol.instance, traffic_lights, id))

    q = []

    for car in cars:
        next_t = car.step(0)
        heapq.heappush(q, (next_t, car.id, car))

    while q:
        time, id, car = heapq.heappop(q)
        if time >= sol.instance.D:
            break
        next_t = car.step(time)
        heapq.heappush(q, (next_t, car.id, car))

    total_score = 0
    finished = 0
    for car in cars:
        if car.score > 0:
            finished+= 1
        total_score += car.score
    print("cars finished:", finished)
    return total_score






if __name__ == "__main__":
    from read_input import Solution
    import cProfile
    #cProfile.run("score= simulate2(Solution.from_argv())")
    score = simulate2(Solution.from_argv())

    print(score)
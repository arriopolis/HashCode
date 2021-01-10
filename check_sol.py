def read_input(filename):
    with open(filename) as fl:
        r,c,fleet,n,bonus,t = map(int,next(fl).strip().split())
        rides = []
        for _ in range(n):
            a,b,x,y,s,f = map(int,next(fl).strip().split())
            rides.append((a,b,x,y,s,f))
    return r,c,fleet,n,bonus,t,rides

def read_submission(filename, f):
    rides = []
    with open(filename) as fl:
        for _ in range(f):
            rides.append(list(map(int,next(fl).strip().split()))[1:])
    return rides

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Supply the input filename and the submission filename as command line arguments.")
        sys.exit()
    r,c,fleet,n,bonus,timelimit,rides = read_input(sys.argv[1])
    routes = read_submission(sys.argv[2], fleet)

    # Check duplicate rides
    visited = set()
    for v in routes:
        assert not visited.intersection(set(v))
        visited.update(v)

    print("Routes visited: {} / {}".format(len(visited), len(rides)))
    for j in set(range(len(rides))).difference(visited):
        print("Route {} not visited with values:".format(j), *rides[j])

    # Check score obtained by vehicle
    score = 0
    bonus_ctr = 0
    for v in routes:
        t = 0
        vx,vy = 0,0
        for ride in v:
            # print("Route:", ride)
            a,b,x,y,s,f = rides[ride]
            t += abs(vx-a) + abs(vy-b)
            vx,vy = a,b
            if t <= s:
                # print("Bonus!")
                score += bonus
                bonus_ctr += 1
                t = s
            # print("Start:", t)
            t += abs(vx-x) + abs(vy-y)
            # print("End:", t)
            if t <= f:
                # print("Score:", abs(vx-x) + abs(vy-y))
                score += abs(vx-x) + abs(vy-y)
            if t > timelimit: break
            vx,vy = x,y
    print("Total score:", score)
    print("Number of bonusses:", bonus_ctr)

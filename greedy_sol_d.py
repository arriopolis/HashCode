from check_sol import read_input

if __name__ == "__main__":
    import sys
    r,c,fleet,n,bonus,timelimit,rides = read_input(sys.argv[1])

    print("Bonus:", bonus)
    print("Fleet:", fleet)
    print("Number of rides:", len(rides))
    print("Timelimit:", timelimit)

    vehicles = [(0,0,0) for _ in range(fleet)]
    res = [[] for _ in range(fleet)]
    jobs = [[] for _ in range(fleet)]
    jobs_done = set()
    job_list = []
    vx,vy,vt = 0,0,0
    for j,(a,b,x,y,s,f) in enumerate(rides):
        length = abs(x-a) + abs(y-b)
        time = max(abs(vx-a) + abs(vy-b), s - vt) + length
        time_waste = max(abs(vx-a) + abs(vy-b), s - vt)
        new_score = length + bonus if abs(vx-a) + abs(vy-b) <= s - vt else length
        if time + vt > f:
            print("Job", j, "is not feasible.")
            continue
        job_list.append((time_waste + .2*length,j,new_score,time+vt))
    job_list.sort()
    for i in range(fleet):
        jobs[i] = job_list.copy()

    score = 0
    while any(jobs):
        i,(_,j,l,vt) = max(((i,job[0]) for i,job in enumerate(jobs) if len(job) > 0), key = lambda x : x[1][0])
        if j in jobs_done:
            jobs[i].pop(0)
            continue
        res[i].append(j)
        jobs_done.add(j)
        score += l
        print("Score:", score, "Jobs remaining:", len(rides) - len(jobs_done), '        ', end = '\r')

        a,b,x,y,s,f = rides[j]
        vehicles[i] = (x,y,vt)
        vx,vy,vt = vehicles[i]
        jobs[i] = []
        for j,(a,b,x,y,s,f) in enumerate(rides):
            if j in jobs_done: continue
            length = abs(x-a) + abs(y-b)
            time = max(abs(vx-a) + abs(vy-b), s - vt) + length
            time_waste = max(abs(vx-a) + abs(vy-b), s - vt)
            new_score = length + bonus if abs(vx-a) + abs(vy-b) <= s - vt else length
            if time + vt > f: continue
            jobs[i].append((time_waste + .2*length,j,new_score,time+vt))
        jobs[i].sort()
    print("Score:", score, '       ')
    print("Number of routes visited:", len(jobs_done))

    with open('res/{}_{}.out'.format(sys.argv[1][0], score), 'w') as f:
        for r in res:
            f.write(' '.join(map(str,[len(r)] + r)) + '\n')

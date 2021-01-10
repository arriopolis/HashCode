from check_sol import read_input

DIST_LIM = 100

if __name__ == "__main__":
    import sys
    r,c,fleet,n,bonus,timelimit,rides = read_input(sys.argv[1])

    edges = []
    for i,(a1,b1,x1,y1,*_) in enumerate(rides):
        print(i, end = '\r')
        edges.append((abs(a1)+abs(b1),0,i))
        for j,(a2,b2,x2,y2,*_) in enumerate(rides):
            if i == j: continue
            dist = abs(x1-a2)+abs(y1-b2)
            if dist <= DIST_LIM:
                edges.append((dist,i,j))
    print(len(edges))
    print("Sorting...")
    edges.sort()

    times = [abs(a)+abs(b)+abs(x-a)+abs(y-b) for a,b,x,y,*_ in rides]
    scores = [abs(x-a)+abs(y-b) for a,b,x,y,*_ in rides]
    ends = list(range(ends))
    starts = list(range(rides))
    num_routes = 0
    for d,i,j in edges:
        if ends[i] != i or start[j] != j: continue
        if ends[j] == j and starts[i] == i and num_routes == fleet: continue
        ends[i] = j
        starts[j] = i
        # times scores

def read_input(filename):
    f = open(filename)
    V,E,R,C,X = map(int,f.readline().strip().split())
    vidsize = [int(x) for x in f.readline().strip().split()]
    endpoints = []

    for i in range(E):
        endpoint_i = []
        endpoint_i.append([int(x) for x in f.readline().strip().split()])
        for j in range(endpoint_i[0][1]):
            endpoint_i.append([int(x) for x in f.readline().strip().split()])
        endpoints.append(endpoint_i)

    requests = []
    for i in range(R):
       requests.append([int(x) for x in f.readline().strip().split()])

    return V,E,R,C,X,vidsize,endpoints,requests

def read_output(filename):
    f = open(filename)
    S = int(f.readline())

    caches = []
    for i in range(S):
        caches.append([int(x) for x in f.readline().strip().split()])

    return S,caches

def calc_score(caches, vidsize, endpoints, requests, V, X):
    # Calculate the score
    for c in caches:
        space = 0
        for vid in c[1:]:
            space += vidsize[vid]

        if space > X:
            print("Cache", c[0], "exceeds the maximum capacity:", space, "MB >", X, "MB")
            sys.exit()


    video_caches = [set() for _ in range(V)]
    for cid,c in enumerate(caches):
        for vid in c[1:]:
            video_caches[vid].add(cid)

    endpoint_caches = [set([c for c,l in endpt[1:]]) for endpt in endpoints]
    endpoint_cache_times = [{c : l for c,l in endpt[1:]} for endpt in endpoints]

    # Calculate score
    scores = []
    N = 0
    for vid,end,n in requests:
        lat_base = endpoints[end][0][0]
        # print(lat_base)
        lat_min = endpoints[end][0][0]
        for cid in endpoint_caches[end].intersection(video_caches[vid]):
            # print(c,endpoints[end][i+1][1],lat_min,lat_base)
            lat_min = min(endpoint_cache_times[end][cid],lat_min)

        scores.append( (lat_base - lat_min)*n )
        N += n
        # print(lat_base,vid,end,N,score)

    res = int(sum(scores)/N*1000)
    print("Average time saved:", res, "microseconds")

    return res

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Supply the input filename and the submission filename as command line arguments.")
        sys.exit()
    V,E,R,C,X,vidsize,endpoints,requests = read_input(sys.argv[1])
    S,caches = read_output(sys.argv[2])

    print("Score:", calc_score(caches, vidsize, endpoints, requests, V, X))

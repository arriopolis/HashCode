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

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Supply the input filename and the submission filename as command line arguments.")
        sys.exit()
    V,E,R,C,X,vidsize,endpoints,requests = read_input(sys.argv[1])
    S,caches = read_output(sys.argv[2])

    for c in caches:
        space = 0
        for vid in c[1:]:
            space += vidsize[vid]

        if space > X:
            print("Cache", c[0], "exceeds the maximum capacity:", space, "MB >", X, "MB")
            sys.exit()


    # Calculate score
    scores = []
    N = 0
    for vid,end,n in requests:
        lat_base = endpoints[end][0][0]
        # print(lat_base)
        lat_min = endpoints[end][0][0]
        for i in range(endpoints[end][0][1]):
            c = endpoints[end][i+1][0]
            for j in caches:
                if c == j[0]:
                    if vid in j[1:]:
                        # print(c,endpoints[end][i+1][1],lat_min,lat_base)
                        lat_min = min(endpoints[end][i+1][1],lat_min)

        scores.append( (lat_base - lat_min)*n )
        N += n
        # print(lat_base,vid,end,N,score)
    print("Average time saved :", int(sum(scores)/N*1000), "microseconds")

    


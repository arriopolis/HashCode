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

if __name__ == "__main__":
    return 0



import sys
from check_sol import read_input

if __name__ == "__main__":
    filename = sys.argv[1]

    v,e,r,c,x,sizes,endpoints,requests = read_input(filename)

    print("Number of videos:", v)
    print("Number of endpoints", e)
    print("Number of requests:", r)
    print("Number of cache servers:", c)
    print("Cache server capacity:", x)
    print("Video sizes ranging between", min(sizes), "and", max(sizes), "Total size:", sum(sizes))
    print("Endpoint latencies ranging between", min(e[0][0] for e in endpoints), "and", max(e[0][0] for e in endpoints))
    print("Cache latencies ranging between", min(l for e in endpoints for c,l in e[1:]), "and", max(l for e in endpoints for c,l in e[1:]))
    print("Number of requests ranging between", min(r[2] for r in requests), "and", max(r[2] for r in requests))
    print("Total number of requests:", sum(r[2] for r in requests))

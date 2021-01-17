import matplotlib.pyplot as plt
import sys
from check_sol import read_input

if __name__ == "__main__":
    filename = sys.argv[1]

    v,e,r,c,x,sizes,endpoints,requests = read_input(filename)

    endpoint_requests = [0]*e
    video_requests = [0]*v
    for vid, eid, num in requests:
        endpoint_requests[eid] += num
        video_requests[vid] += num

    endpoint_cache_connections = [0]*e
    cache_endpoint_connections = [0]*c
    for eid,endpt in enumerate(endpoints):
        for cid,_ in endpt[1:]:
            endpoint_cache_connections[eid] += 1
            cache_endpoint_connections[cid] += 1

    endpoint_latencies = [endpt[0][0] for endpt in endpoints]*e

    # print("Number of videos:", v)
    # print("Number of endpoints", e)
    # print("Number of requests:", r)
    # print("Number of cache servers:", c)
    # print("Cache server capacity:", x)
    # print("Video sizes ranging between", min(sizes), "and", max(sizes))
    # print("Endpoint latencies ranging between", min(e[0][0] for e in endpoints), "and", max(e[0][0] for e in endpoints))
    # print("Cache latencies ranging between", min(l for e in endpoints for c,l in e[1:]), "and", max(l for e in endpoints for c,l in e[1:]))
    # print("Number of requests ranging between", min(r[2] for r in requests), "and", max(r[2] for r in requests))

    fig = plt.figure()
    ax = fig.gca()
    ax.hist(sizes)
    ax.set_title('Video sizes')

    fig = plt.figure()
    ax = fig.gca()
    ax.bar(range(e), endpoint_requests)
    ax.set_title('Number of requests per endpoint')

    fig = plt.figure()
    ax = fig.gca()
    ax.bar(range(v), video_requests)
    ax.set_title('Number of requests per video')

    fig = plt.figure()
    ax = fig.gca()
    ax.bar(range(e), endpoint_cache_connections)
    ax.set_title('Number of cache servers per endpoint')

    fig = plt.figure()
    ax = fig.gca()
    ax.bar(range(c), cache_endpoint_connections)
    ax.set_title('Number of endpoint per cache servers')

    fig = plt.figure()
    ax = fig.gca()
    ax.hist(endpoint_latencies)
    ax.set_title('Latencies of endpoints')

    plt.show()

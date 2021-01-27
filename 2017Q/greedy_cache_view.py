from check_sol import read_input
import time
import sys
import heapq
V,E,R,C,X,vidsize,endpoints,requests = read_input(sys.argv[1])

endpoint_latencies = [{c : l for c,l in endpt[1:]} for endpt in endpoints]
tot_requests = sum(r[2] for r in requests)
print("Total number of requests:", tot_requests)

benefits = {}
for i,(v_id, e_id, num_req) in enumerate(requests):
    if i%1000 ==0:
        print(i+1, '/', len(requests), '            ',  end = '\r')
    base_lat = endpoints[e_id][0][0]
    for c_id, lat in endpoints[e_id][1:]:
        if (v_id,c_id) not in benefits: benefits[(v_id,c_id)] = [0,[]]
        benefits[(v_id,c_id)][0] += (base_lat - lat)*num_req/vidsize[v_id]
        benefits[(v_id,c_id)][1].append((e_id,num_req,-1))
q = sorted((-benefit,(v_id,c_id),endpts) for (v_id,c_id),[benefit,endpts] in benefits.items())

cache_size_left = [X for i in range(C)] # size of cache
videos_in_cache = [set() for i in range(C)] # videos in cache
score = 0
while q:
    diff,(v_id,c_id),endpts = heapq.heappop(q)
    print(f"Trying to insert {v_id} into {c_id}. Reported benefit: {-diff*1000/tot_requests}.", end = '\r')

    # Check if it still fits
    if cache_size_left[c_id] < vidsize[v_id]: continue
    # print("This fits.")

    # Check if the current metric is still up to date
    toreplace = {}
    for (endpt,num_req,prev) in endpts:
        if any(v_id in videos_in_cache[c] for c,l in endpoints[endpt][1:]):
            l,c = min((l,c) for c,l in endpoints[endpt][1:] if v_id in videos_in_cache[c])
            oldl = endpoint_latencies[endpt][prev] if prev != -1 else endpoints[endpt][0][0]
            if l < endpoint_latencies[endpt][c_id]:
                diff += (oldl - endpoint_latencies[endpt][c_id]) * num_req/vidsize[v_id]
                toreplace[(endpt,num_req,prev)] = None
            elif l < oldl:
                diff += (oldl - l) * num_req/vidsize[v_id]
                toreplace[(endpt,num_req,prev)] = (endpt,num_req,c)

    if toreplace:
        # print("The following endpoints no longer benefit from this:", toreplace)
        for x,y in toreplace.items():
            endpts.remove(x)
            if y is not None: endpts.append(y)
        # print("New entry:", (diff, (v_id,c_id), endpts))
        if diff < 0: heapq.heappush(q, (diff, (v_id,c_id), endpts))
        continue

    videos_in_cache[c_id].add(v_id)
    cache_size_left[c_id] -= vidsize[v_id]
    score -= diff
    print()
    print("New score:", score * 1000 / tot_requests)
print(score)
print("Normalized score:", score * 1000 / tot_requests)

caches = [[i]+list(cache) for i, cache in enumerate(videos_in_cache)]
import os
from check_sol_v2 import calc_score

score = calc_score(caches, vidsize, endpoints, requests, V, X)
print(score)
file_name = os.path.join("output", '.'.join(sys.argv[1].split('.')[:-1])+'_'+str(score)+'.out')
with open(file_name, 'w') as f:
    f.write(str(len(videos_in_cache))+"\n")
    for c_id, videos in enumerate(videos_in_cache):
        f.write(f"{c_id} {' '.join(map(str,videos))}"+"\n")

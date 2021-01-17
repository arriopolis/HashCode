from check_sol import read_input
import time
import sys
print(sys.argv[0])
V,E,R,C,X,vidsize,endpoints,requests = read_input(sys.argv[1])


#                               c_id     datac_lat        c_late
endpoint_cache_latency = {
        e_id:sorted([[cache[0], endpoint[0][0] - cache[1]] for cache in endpoint[1:]], key = lambda x: -x[1]) for e_id, endpoint in enumerate(endpoints)}

# Calc metric for all requests



max_endpoint_latency = {}

for e_id, endpoint in enumerate(endpoints):
    datacenter_latency, n_caches = endpoint[0]
    if n_caches  == 0:
        max_endpoint_latency[e_id] = [-1, 1000000000000]
    else:
        max_latency  = max(endpoint[1:], key = lambda x: datacenter_latency-x[1])
        max_endpoint_latency[e_id] = [max_latency[0], endpoint[0][0]-max_latency[1]]

t = time.time()
request_with_metric = []
for v_id, e_id, num_req in requests:
    # latency metric
    metric = num_req*max_endpoint_latency[e_id][1]

    request_with_metric.append([v_id, e_id, num_req, metric, max_endpoint_latency[e_id][0]])
print(time.time() -t)

#sort by metric
request_with_metric = sorted(request_with_metric, key = lambda x: x[3])[::-1]
print(request_with_metric[:10])



# add request to cache
cache_size_left = [X for i in range(C)] # size of cache
videos_in_cache = [set() for i in range(C)] # videos in cache
print("n_metrics:", len(request_with_metric))
k =0
while len(request_with_metric) > 0:
    k+=1
    if (k %1000 == 0):
        print(k,len(request_with_metric), "left")
    v_id, e_id, num_req, metric, c_id = request_with_metric.pop(0)
    if c_id == -1:
        continue
    # check if request is still valid
    if v_id in videos_in_cache[c_id]:
        continue
    if cache_size_left[c_id] < vidsize[v_id]:
        # recalculate metric
        for c_id, latency in endpoint_cache_latency[e_id]:
            if cache_size_left[c_id] >= vidsize[v_id]:
                break
        else:
            continue
        metric = num_req * latency
        # insert at correct position
        for i, target in enumerate(request_with_metric):
            if target[3] < metric:
                break
        request_with_metric.insert(i, [v_id, e_id, num_req, metric, c_id])
        continue
    # add video to cache:
    videos_in_cache[c_id].add(v_id)
    cache_size_left[c_id] -= vidsize[v_id]

import os
file_name = os.path.join("output", '.'.join(sys.argv[1].split('.')[:-1])+'.out')
with open(file_name, 'w') as f:
    f.write(str(len(videos_in_cache))+"\n")
    for c_id, videos in enumerate(videos_in_cache):
        f.write(f"{c_id} {' '.join(map(str,videos))}"+"\n")



# for request in sorted list:
    #

from check_sol_v2 import read_input, calc_score

filename = 'trending_today.in'
V,E,R,C,X,vidsize,endpoints,requests = read_input(filename)
print("Capacity:", X)

vidsizes = {}
for vid,v in enumerate(vidsize):
    if v not in vidsizes: vidsizes[v] = []
    vidsizes[v].append(vid)

ctr = 0
caches = []
while ctr < C and vidsizes:
    cache_set = set()
    w = 0
    while any(v <= X-w for v in vidsizes):
        v = max(v for v in vidsizes if v <= X-w)
        vid = vidsizes[v].pop()
        if len(vidsizes[v]) == 0: del vidsizes[v]
        w += v
        cache_set.add(vid)
    caches.append([len(caches)] + list(cache_set))
    print(w, len(cache_set))
    ctr += 1

print("Items left:", ','.join(map(str,[v for vids in vidsizes.values() for v in vids])))
print("Number of bins used:", ctr)

score = calc_score(caches, vidsize, endpoints, requests, V, X)
print("Score:", score)

import os
file_name = os.path.join("output", '.'.join(filename.split('.')[:-1]) + '_' + str(score) + '.out')
with open(file_name, 'w') as f:
    f.write(str(len(caches))+"\n")
    for videos in caches:
        f.write(f"{' '.join(map(str,videos))}"+"\n")

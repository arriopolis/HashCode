from check_sol_v2 import read_input, calc_score

V,E,R,C,X,vidsize,endpoints,requests = read_input('trending_today.in')
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
    caches.append(list(cache_set))
    print(w, len(cache_set))
    ctr += 1

print("Items left:", ','.join(map(str,[v for vids in vidsizes.values() for v in vids])))
print(ctr)

print("Score:", calc_score(caches, vidsize, endpoints, requests, V, X))

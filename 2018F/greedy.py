import sys
import numpy as np
np.set_printoptions(linewidth=200)
from diamant import diamant
from read_input import read_input
from scipy.signal import convolve2d

filename = sys.argv[1]
h,w,d,b,residentials,services = read_input(filename)

def reachable_block(block):
    hp,wp = len(block), len(block[0])
    res = np.zeros((hp+2*d,wp+2*d), dtype = np.bool_)
    for i,r in enumerate(block):
        for j,c in enumerate(r):
            if c:
                res[i:i+2*d+1,j:j+2*d+1] |= diamant(d)
    res[d:d+hp,d:d+wp] = False
    return res

def neighborhood(pos,d):
    i,j = pos
    for dy in range(-d,d+1):
        if i+dy < 0 or i+dy >= h: continue
        rem = d-abs(dy)
        for dx in range(-rem,rem+1):
            if j+dx < 0 or j+dx >= w: continue
            yield i+dy,j+dx

uts = []
for idx,_,_,t,block in services:
    s = sum(1 if c else 0 for r in block for c in r)
    uts.append((s,t,idx,np.array(block),reachable_block(block)))
uts.sort()
service_types = set([t for _,t,_,_,_ in uts])

grid = np.zeros((h,w), dtype = np.bool_)
covered = {t : np.array(grid) for t in service_types}

buildings = []
while uts:
    s,t,idx,block,reachable = uts.pop(0)
    print("Number of service stations left:", len(uts))
    while True:
        print("Number of buildings placed:", len(buildings))
        placeable = convolve2d(np.logical_not(grid).astype(int), block.astype(int))[block.shape[0]-1:, block.shape[1]-1:] == s
        # print("Placeable:")
        # print(placeable)
        score = convolve2d(np.logical_not(np.logical_or(grid,covered[t])).astype(int), reachable.astype(int))[block.shape[0]-1+d:-d, block.shape[1]-1+d:-d]
        # print("Score:")
        # print(score)
        potential_lost = sum(convolve2d(c.astype(int), block.astype(int))[block.shape[0]-1:, block.shape[1]-1:] for c in covered.values())
        # print("Potential lost:")
        # print(potential_lost)
        benefit = (score - potential_lost) * placeable.astype(int)
        # print("Benefit:")
        # print(benefit)
        i,j = np.unravel_index(np.argmax(benefit), benefit.shape)
        if benefit[i,j] <= 0: break

        grid[i:i+block.shape[0], j:j+block.shape[1]] |= block
        covered[t][max(i-d,0):min(i+block.shape[0]+d,h), max(j-d,0):min(j+block.shape[1]+d,w)] |= np.logical_and(np.logical_not(grid[max(i-d,0):min(i+block.shape[0]+d,h), max(j-d,0):min(j+block.shape[1]+d,w)]), reachable[max(0,d-i):min(reachable.shape[0],h-i+d),max(0,d-j):min(reachable.shape[1],w-j+d)])

        buildings.append((idx,i,j))

        # print("New grid:")
        # print(grid)
        # print("New covered:")
        # print(covered[t])

print(buildings)

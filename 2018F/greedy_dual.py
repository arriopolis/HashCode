from read_input import read_input
import sys
import numpy as np
from scipy.signal import convolve2d
filename = sys.argv[1]
origh,origw,d,b,residentials,services = read_input(sys.argv[1])

residentialsorig = residentials
servicesorig = services

h = w = 20

def buffer(plan):
    plan = np.vstack([np.zeros(shape=[d, plan.shape[1]]), plan, np.zeros(shape=[d, plan.shape[1]])])
    plan = np.hstack([np.zeros(shape=[plan.shape[0], d]), plan, np.zeros(shape=[plan.shape[0], d])])
    return plan

DIAMOND = (np.abs(np.arange(2*d+1)-d)[:,np.newaxis] + np.abs(np.arange(2*d+1)-d)[np.newaxis,:] <= d).astype(int)

def diamond_buffer(plan):
   return  (convolve2d(plan, DIAMOND, "full")>0).astype(int)

service_types = set([service[3] for service in services])

residentials = [[*r[:4], np.array(r[4], dtype=int), diamond_buffer(np.array(r[4], dtype=int))] for r in residentials]
services = [[*r[:4], np.array(r[4], dtype=int), diamond_buffer(np.array(r[4], dtype=int))] for r in services]

print(service_types)
service_maps = {t: np.zeros(shape =[h+2*d,w+2*d], dtype = int)for t in service_types}
residential_map = np.zeros(shape = [h+2*d,w+2*d], dtype = int)
occupancy_map = np.ones(shape = [h,w], dtype = int)

added_residentials = []

buildings = []

def has_positions(plan):
    available =  convolve2d(occupancy_map, plan[::-1,::-1], 'full')[plan.shape[0]-1:, plan.shape[1]-1:] == plan.sum()
    return available

def calc_high_score_service(service):
    count, hp, wp, cp, plan, reach_map = service
    positions = zip(*np.where(has_positions(plan)))
    maxi= -1
    maxj= -1
    maxv = -1
    print( "poss:", list(positions)[:10])
    for i,j in zip(*np.where(has_positions(plan))):
        buildings = set((residential_map[i:i+reach_map.shape[0], j:j+reach_map.shape[1]]*(reach_map-service_maps[cp][i:i+reach_map.shape[0], j:j+reach_map.shape[1]]*reach_map)).flatten())
        if 0 in buildings:
            buildings.remove(0)
        if -1 in buildings:
            buildings.remove(-1)
        try:
            v = sum([added_residentials[b-1][3] for b in buildings])
        except Exception as e:
            print(buildings)
            raise e
        if maxv < v:
            maxi,maxj,maxv = i,j,v
    return maxi,maxj,maxv


def calc_high_score_residential(residential):
    count, hp, wp, cp, plan, reach_map = residential
    point_map = np.zeros(shape = [h,w], dtype=int)
    for r, service_map in service_maps.items():

        point_map += (convolve2d(service_map[d:-d,d:-d], plan[::-1,::-1], 'full')[plan.shape[0]-1:, plan.shape[1]-1:]>0).astype(int)
    point_map *= has_positions(plan).astype(int)
    #point_map += has_positions(plan).astype(int)-1
    maxv = point_map.max()
    i,j = np.where(point_map == maxv)
    return i[0],j[0],maxv


def add_service(service,i,j):
    print("Adding service")
    global occupancy_map, buildings
    count, hp, wp, cp, plan, reach_map = service
    print(occupancy_map[i:i + plan.shape[0], j:j + plan.shape[1]])
    print(plan)
    assert np.sum(plan * occupancy_map[i:i + plan.shape[0], j:j + plan.shape[1]]) == np.sum(plan)

    occupancy_map[i:i + plan.shape[0], j:j + plan.shape[1]] -= plan

    service_maps[cp][i:i + reach_map.shape[0], j:j + reach_map.shape[1]]  += reach_map

    buildings += [(service[0],i,j)]


def add_residential(residential,i,j):
    global occupancy_map, residential_map, buildings
    count, hp, wp, cp, plan, reach_map = residential
    print(occupancy_map[i:i + plan.shape[0], j:j + plan.shape[1]])
    print(plan)
    print(has_positions(plan).astype(int))
    print(occupancy_map)
    assert np.sum(plan * occupancy_map[i:i + plan.shape[0], j:j + plan.shape[1]]) == np.sum(plan)
    occupancy_map[i:i + plan.shape[0], j:j + plan.shape[1]] -= plan

    residential_map[i + d:i + d + plan.shape[0], j + d:j + d + plan.shape[1]] += plan*(len(added_residentials) + 1)
    added_residentials.append(residential)
    buildings += [(residential[0], i, j)]

add_residential(residentials[0],0,0)
print(residential_map[d:,d:])


score = 0
while True:
    maxv = -1
    maxobj = None
    maxi = maxj = -1
    maxtype = None
    print("running residentials")
    for residential in residentials:
        i,j,v = calc_high_score_residential(residential)
        if v > maxv:
            maxobj = residential
            maxtype = "residential"
            maxi = i
            maxj = j
            maxv = v
    print(maxv)
    print("running services")
    for service in services:
        i,j,v = calc_high_score_service(service)
        if v > maxv:
            maxobj = service
            maxtype = "service"
            maxi = i
            maxj = j
            maxv = v
    print(maxv)
    if maxv <=0:
        print("nothing found")
        break
    if maxtype == "residential":
        add_residential(maxobj, maxi,maxj)
    else:
        add_service(maxobj,maxi,maxj)

    score += maxv
    print("added")
from calc_score import calc_score
score = calc_score(h, w, d, b, residentialsorig, servicesorig, buildings) * (origh // h) * (origw // w)
print("score", score)
print()


print()

residentials = residentialsorig
services = servicesorig

new_buildings = []
for idx,i,j in buildings:
    for k in range(origh//h):
        for l in range(origw//w):
            new_buildings.append((idx,k*h+i,l*w+j))
buildings = new_buildings
# sol.print()

score = calc_score(origh, origw, d, b, residentials, services, buildings)
print("Score:", score)
with open('res/{}_{}.txt'.format(filename.split('/')[-1][0], score), 'w') as f:
    f.write(str(len(buildings)) + '\n')
    for idx,i,j in buildings:
        f.write('{} {} {}\n'.format(idx, i, j))


















from check_sol import read_input
from check_sol import read_output
from check_sol_v2 import calc_score
from copy import deepcopy

import sys
import os

V = []
E = []
R = []
C = []
X = []
vidsize = []
endpoints = []
requests = []

def deltaremovevideofromcache(S, caches):
    bestdelta = -pow(10,6)

    bestremovalcache = caches
    initialScore = calc_score(caches, vidsize, endpoints, requests, V, X)

    for ci, c in enumerate(caches):
        popindices = []

        for vi, v in enumerate(c[1:]):
            tempcaches = deepcopy(caches)
            tempcaches[ci].pop(vi + 1)
            score = calc_score(tempcaches, vidsize, endpoints, requests, V, X)
            delta = score - initialScore

            print("Cost for removing video " + str(v) + " from cache " + str(c[0]) + " is " + str(delta) + ".\n")

            if delta > -5:
                popindices += [vi+1]

        popindices.reverse()
        print(popindices)
        for pi in popindices:
            caches[ci].pop(pi)

    return caches

if __name__ == "__main__":
    # inputfile = "example.in"
    # outputfile = "example.out"

    inputfile = "kittens.in"
    outputfile = "output/kittens.in.out"

    # inputfile = "kittens.in"
    # outputfile = "output/kittens.in.out"

    V, E, R, C, X, vidsize, endpoints, requests = read_input(inputfile)
    S, caches = read_output(outputfile)

    print(caches)
    caches = deltaremovevideofromcache(S, caches)
    print(caches)

    file_name = os.path.join("output", '.'.join(outputfile.split('.')[:-1]) + '.reduced.out')
    with open(file_name, 'w') as f:
        f.write(str(len(caches)) + "\n")
        for c_id, videos in enumerate(caches):
            if len(caches[c_id]) > 1:
                f.write(f"{c_id} {' '.join(map(str, videos))}" + "\n")



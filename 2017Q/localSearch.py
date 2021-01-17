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

            if delta > -15000:
                popindices += [vi+1]

        popindices.reverse()
        print(popindices)
        for pi in popindices:
            caches[ci].pop(pi)

    return caches

if __name__ == "__main__":
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    # inputfile = "example.in"
    # outputfile = "example.out"

    # inputfile = "me_at_the_zoo.in"
    # outputfile = "output/me_at_the_zoo.reduced.out"

    # inputfile = "kittens.in"
    # outputfile = "output/kittens.in.out"

    V, E, R, C, X, vidsize, endpoints, requests = read_input(inputfile)
    S, caches = read_output(outputfile)

    print(caches)
    caches = deltaremovevideofromcache(S, caches)
    print(caches)

    file_name = os.path.join(outputfile[:-4]) + "_" + str(calc_score(caches, vidsize, endpoints, requests, V, X)) + '.reduced.out'
    with open(file_name, 'w') as f:
        f.write(str(len(caches)) + "\n")
        for c_id, videos in enumerate(caches):
            if len(caches[c_id]) > 1:
                f.write(f"{videos[0]} {' '.join(map(str, videos[1:]))}" + "\n")



from read_input import Input, Solution
from collections import defaultdict, Counter
import numpy as np
import heapq

inp = Input.from_argv()


time = 0
score =0
for dt in sorted([lib[0] for lib in inp.libraries]):
    time += dt
    if time <= inp.D:
        score += 1000-time
print(score)
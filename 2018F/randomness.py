import random,sys
from read_input import read_input
# from read_solution import Solution
from calc_score import calc_score

filename = sys.argv[1]
h,w,d,b,residentials,services = read_input(filename)
# sol = Solution(sys.argv[1])

grid = [[False]*w for _ in range(h)]
buildings = []
print("Keyboard interrupt once you're satisfied.")
score = 0
try:
    while True:
        idx,_,_,_,block = random.choice(residentials) if random.random() < .5 else random.choice(services)
        i,j = random.randint(0,h),random.randint(0,w)
        fit = True
        for di,r in enumerate(block):
            for dj,c in enumerate(r):
                if i+di >= h or j+dj >= w or grid[i+di][j+dj]:
                    fit = False
                    break
            if not fit: break
        if not fit: continue
        buildings.append((idx,i,j))
        for di,r in enumerate(block):
            for dj,c in enumerate(r):
                grid[i+di][j+dj] = True
        if len(buildings)%10000 == 0:
            # sol.constructed_buildings = buildings
            # score = sol.determine_score()
            score = calc_score(h, w, d, b, residentials, services, buildings)
        print("Number of buildings placed:", len(buildings), "Last calculated score:", score, end = '\r')
except KeyboardInterrupt:
    print()
    print('\n'.join(''.join('#' if c else '.' for c in r) for r in grid))

    # sol.print()

    with open('res/{}_{}.txt'.format(filename.split('/')[-1][0], score), 'w') as f:
        f.write(str(len(buildings)) + '\n')
        for idx,i,j in buildings:
            f.write('{} {} {}\n'.format(idx, i, j))

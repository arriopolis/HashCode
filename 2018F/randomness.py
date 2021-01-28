import random,sys
from read_input import read_input
# from read_solution import Solution
from calc_score import calc_score

filename = sys.argv[1]
origh,origw,d,b,residentials,services = read_input(filename)
# sol = Solution(sys.argv[1])

h,w = [int(sys.argv[2])]*2
print(h,w)

print("Keyboard interrupt once you're satisfied.")
best_score = (-1,None,None)
try:
    while True:
        score = 0
        grid = [[False]*w for _ in range(h)]
        buildings = []
        non_changed_iterations = 0
        while non_changed_iterations < 1000:
            non_changed_iterations += 1
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
            score = calc_score(h, w, d, b, residentials, services, buildings) * (origh // h) * (origw // w)
            non_changed_iterations = 0
            print("Number of buildings placed:", len(buildings), "Last calculated score:", score, '                     ', end = '\r')
        if score > best_score[0]:
            print("Reported benefit's best score so far:", score, '                         ')
        best_score = max(best_score, (score, buildings, grid))
except KeyboardInterrupt:
    buildings = best_score[1]
    grid = best_score[2]

    print()
    print('\n'.join(''.join('#' if c else '.' for c in r) for r in grid))
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

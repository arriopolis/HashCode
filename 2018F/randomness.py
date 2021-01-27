import random,sys
from read_input import read_input

filename = sys.argv[1]
h,w,d,b,residentials,services = read_input(filename)

grid = [[False]*w for _ in range(h)]
buildings = []
print("Keyboard interrupt once you're satisfied.")
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
        print("Number of buildings placed:", len(buildings), end = '\r')
except KeyboardInterrupt:
    print()
    print('\n'.join(''.join('#' if c else '.' for c in r) for r in grid))

    with open('res_{}'.format(filename.split('/')[-1]).replace('.in','.txt'), 'w') as f:
        f.write(str(len(buildings)) + '\n')
        for idx,i,j in buildings:
            f.write('{} {} {}\n'.format(idx, i, j))

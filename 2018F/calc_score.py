import sys
from read_input import read_input

def calc_score(h, w, d, b, residentials, services, buildings, debug = False):
    plans = [None]*max(idx+1 for idx,*_ in residentials + services)
    for idx,hp,wp,cp,block in residentials:
        plans[idx] = ('R',hp,wp,cp,block)
    for idx,hp,wp,tp,block in services:
        plans[idx] = ('U',hp,wp,tp,block)
    grid = [[0]*w for _ in range(h)]
    for idx,i,j in buildings:
        for di,r in enumerate(plans[idx][4]):
            for dj,c in enumerate(r):
                if not c: continue
                if grid[i+di][j+dj] != 0:
                    print("There is overlap.")
                    sys.exit()
                grid[i+di][j+dj] = -1 if plans[idx][0] == 'R' else plans[idx][3]
    # print('\n'.join(''.join(str(c) if c != -1 else '.' for c in r) for r in grid))

    score = 0
    for ctr,(idx,k,l) in enumerate(buildings):
        if plans[idx][0] == 'U': continue
        for di,r in enumerate(plans[idx][4]):
            for dj,c in enumerate(r):
                i,j = k+di,l+dj
                ss = set()
                for di in range(-d,d+1):
                    if i+di >= h: break
                    if i+di < 0: continue
                    rem = d-abs(di)
                    for dj in range(-rem,rem+1):
                        if j+dj >= w: break
                        if j+dj < 0: continue
                        if grid[i+di][j+dj] not in (0,-1):
                            ss.add(grid[i+di][j+dj])
        if debug: print("Progress:", ctr, end = '\r')
        # print(idx,i,j,ss)
        score += len(ss) * plans[idx][3]
    if debug: print()
    if debug: print("Score:", score)
    return score

if __name__ == "__main__":
    input_filename = sys.argv[1]
    h,w,d,b,residentials,services = read_input(input_filename)
    # print(residentials)

    sol_filename = sys.argv[2]
    buildings = []
    with open(sol_filename) as f:
        buildings = [tuple(map(int,line.strip().split())) for line in f.readlines()[1:]]
    # print(buildings)

    print(calc_score(h, w, d, b, residentials, services, buildings))

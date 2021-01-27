def read_input(filename):
    residentials, services = [], []

    with open(filename, 'r') as f:
        h,w,d,b = map(int,next(f).strip().split())
        for _ in range(b):
            tp,hp,wp,cp = next(f).strip().split()
            block = []
            for _ in range(int(hp)):
                block.append([c == '#' for c in next(f).strip()])
            if tp == 'R':
                residentials.append((int(hp),int(wp),int(cp),block))
            else:
                services.append((int(hp),int(wp),int(cp),block))
    return h,w,d,b,residentials,services

if __name__ == '__main__':
    import sys
    residentials, services = read_input(sys.argv[1])
    print("Residentials:")
    print('\n'.join(map(str,residentials)))
    print("Services:")
    print('\n'.join(map(str,services)))

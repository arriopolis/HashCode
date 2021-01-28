def read_input(filename):
    residentials, services = [], []

    with open(filename, 'r') as f:
        h,w,d,b = map(int,next(f).strip().split())
        count = 0
        for _ in range(b):
            tp,hp,wp,cp = next(f).strip().split()
            block = []

            for _ in range(int(hp)):
                block.append([c == '#' for c in next(f).strip()])
            if tp == 'R':
                residentials.append((count, int(hp),int(wp),int(cp),block))
            else:
                services.append((count, int(hp),int(wp),int(cp),block))
            count += 1
    # return h,w,d,b,reduce_same_layouts(residentials),reduce_same_layouts(services)
    return h,w,d,b,reduce_same_layouts(residentials),services


def reduce_same_layouts(layouts):
    reduced_layouts = []

    while len(layouts) != 0:
        best_layout = layouts[0]
        idx, hp, wp, cp, layout = layouts[0]

        layouts_to_delete = []
        for r in layouts:
            if layout == r[4]:
                layouts_to_delete.append(r)
                if best_layout[3] < r[3]:
                    best_layout = r

        for r in layouts_to_delete:
            layouts.remove(r)
        reduced_layouts.append(best_layout)

    return reduced_layouts


if __name__ == '__main__':
    import sys
    h,w,d,b,residentials, services = read_input(sys.argv[1])
    print("Residentials:")
    print('\n'.join(map(str,residentials)))
    print("Services:")
    print('\n'.join(map(str,services)))

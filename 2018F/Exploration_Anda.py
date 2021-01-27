def highest_density(residentials):
    for i, r in enumerate(residentials):
        residentials[i] = list(residentials[i]) + [r[2] / sum([sum(y) for y in r[3]])]

    # print(residentials)
    sorted_residentials = sorted(residentials, key=lambda x: x[4], reverse=True)

    for r in sorted_residentials:
        print(r[0:3], r[4])
        print_plan(r[3])


def print_plan(block):
    for row in block:
        for x in row:
            if x:
                print('#', end='')
            else:
                print('.', end='')
        print('\n', end='')

if __name__ == '__main__':
    import sys
    from read_input import read_input,reduce_same_layouts
    from read_solution import Solution

    # h, w, d, b, residentials, services = read_input(sys.argv[1])

    solution = Solution(sys.argv[1])
    solution.read_solution(sys.argv[2])
    print(solution.determine_score())



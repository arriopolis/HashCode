import matplotlib.pyplot as plt
from check_sol import read_input, read_submission

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

if __name__ == "__main__":
    import sys
    r,c,fleet,n,bonus,timelimit,rides = read_input(sys.argv[1])
    routes = read_submission(sys.argv[2], fleet)

    fig = plt.figure()
    ax = fig.gca()
    for ride in rides:
        a,b,x,y,s,f = ride
        # ax.plot([a,x],[b,y], 'black', alpha = .3)
        ax.plot(a, b, '.g',  markersize = 12)
        ax.plot(x, y, '.r',  markersize = 12)
    ax.set_title(sys.argv[1])

    for i,v in enumerate(routes):
        if not v: continue
        a,b,x,y,*_ = rides[v[0]]
        ax.plot([0,a], [0,b], color = colors[i%len(colors)])
        for j,k in zip(v[:-1], v[1:]):
            a1,b1,x1,y1,*_ = rides[j]
            a2,b2,x2,y2,*_ = rides[k]
            ax.plot([x1,a2], [y1,b2], color = colors[i%len(colors)])
    plt.show()

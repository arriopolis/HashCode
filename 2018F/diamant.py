import numpy as np

diamant = lambda d : (np.abs(np.arange(2*d+1)-d)[:,np.newaxis] + np.abs(np.arange(2*d+1)-d)[np.newaxis,:] <= d)

if __name__ == '__main__':
    print(diamant(5))

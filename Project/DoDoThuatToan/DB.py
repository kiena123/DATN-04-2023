import math
import numpy as np

def DB(data, numClust, center, U):
    def d( X1, l, m):
        return np.linalg.norm(X1[l] - X1[m])

    def d1( X, X1, C, l):
        N = len(X)
        return sum(np.linalg.norm(Xi - X1[l]) for Xi in C[l])/N[l]

    def D(X, X1, C, l, m):
        N = len(X)
        __Tu = d1(N, C, X, X1, l) + d1(N, C, X, X1, m)
        __Mau = d( X1, l, m)
        return __Tu / __Mau

    sum1 = 0
    for j in range(numClust):
        D = -1
        for l in range(j):
            for m in range(j):
                if ( l != m):
                    D = max( D, D(data, numClust, center, l, m))

        sum1 += D

    return sum1/numClust

DB()

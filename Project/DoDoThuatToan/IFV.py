import numpy as np
import math

def IFV( X, V, C, U):
    def SDmax(V, j):
        listSD = list()
        for k in range(j):
            for i in range(j):
               if(i != k):
                  listSD.append(pow(np.linalg.norm(V[k] - V[i]), 2))
                  
        return max(listSD)
    
    def Sigma1D(X, V, C, N):
        sum1 = 0;
        for j in range(C):
            sum2 = 0
            for k in range(N):
                sum2 += pow(np.linalg.norm(X[k] - V[j]), 2)
            sum1 += sum2/N
        return sum1/C

    ###

    sum1 = 0
    for j in range(C):
        sum2 = 0
        for k in range(N):
            sum3 = 0
            for k in range(N):
                sum3 += math.log(U[k, j], 2)
            sum2 += pow(U[k, j], 2) * pow(math.log(C, 2) - sum3/N, 2)

        __TuSo = SDmax(V, j)
        __MauSo = Sigma1D(X, V, C, len(X))
        sum1 += sum2/N*__TuSo/__MauSo

    return sum1/C

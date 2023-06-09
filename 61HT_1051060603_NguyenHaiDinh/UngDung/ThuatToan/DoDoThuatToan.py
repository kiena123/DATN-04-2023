import math
import numpy as np

###
''' Do Do Thuat Toan DB '''
###
def DB(data, center, numClust, U):
    N, r = data.shape
    maxU = max(np.unique(U))

    S = np.zeros(shape = numClust)
    
    for j in range(numClust):
        index = np.where(U[:, j] == maxU)[0]
        for i in index:
            S[j] += pow(np.linalg.norm(data[i] - center[j]), 2)
        S[j] = pow(S[j]/N, 1/2)
        
    DB_value = 0
    
    for l in range(numClust):
        maxSM = 0;
        for m in range(numClust):
            if ( l != m):
                temp = (S[l] + S[m])/np.linalg.norm(center[l] - center[m])
                maxSM = max(maxSM, temp)
        DB_value += maxSM
        
    return DB_value/numClust

###
''' Do Do Thuat Toan IFV '''
###
def IFV( X, V, C, U):
    N, r = X.shape
    sigmaD = 0;
    sum1 = 0;
    eps = 0.0001
    
    for j in range(C):
        sum2 = 0
        sum3 = 0
        for k in range(N):
            if U[k, j] == float(0):
                U[k, j] = eps
                
            if U[k, j] == float(1):
                U[k, j] = 1 - eps

            # sum2 += math.log(U[k, j])/math.log(2)
            sum2 += math.log(U[k, j], 2)
            sum3 += pow( U[k, j], 2)
            sigmaD += pow( np.linalg.norm(X[k] - V[j]), 2)

        sum2 = pow( math.log(C, 2) - sum2/N,2)
        sum3 = sum3 / N

        sum1 += sum2 * sum3

    sigmaD = sigmaD/(N * C)

    calcSDmax = 0;
    for i in range(C - 1):
        for j in range(i+1, C):
            calcSDmax = max(calcSDmax, pow(np.linalg.norm(V[i] - V[j]), 2))

    return (sum1 * calcSDmax) / ( sigmaD * C)

###
''' Do Do Thuat Toan PDM '''
###
def PDM( X, X1, k, U ):
    N, r = X.shape
    maxU = max(np.unique(U))
    
    def E1():
        sum1 = 0
        for i in range(N):
            sum1 += np.linalg.norm(X[i] - X1)
        return sum1

    def Ek():
        sum1 = 0
        for l in range(k):
            index = np.where(U[:, l] == maxU)[0]
            clustData = X[index, :]
            sum1 += np.linalg.norm(clustData - X1[l])
        return sum1

    def Dk():
        __Dk = 0
        for l in range(k - 1):
            for m in range( l+1, k):
                __Dk = max(__Dk, np.linalg.norm(X1[l] - X1[m]))
        return __Dk

    __E1 = E1()
    __Ek = Ek()
    __Dk = Dk()
    return pow((__E1*__Dk)/(__Ek*k), 2)

###
''' Do Do Thuat Toan SSWC '''
###
def SSWC(X, X1, C, U):
    maxU = max(np.unique(U))
    SSWC_value = 0
    for j in range(C):
        index = np.where(U[:, j] == maxU)[0]

        if len(index) == 1:
            continue
        
        clustData = X[index, :]
        
        for i in index:
            __Aji = sum(np.linalg.norm(val - X[i, :]) for val in clustData)/len(index)
            __Bji = 10^6

            for k in range(C):
                if k != j :
                    indexK = np.where(U[:, k] == maxU)[0]
                    clustDataK = X[indexK, :]
                    if len(indexK) > 0:
                        __Dki = sum(np.linalg.norm(val - X[i, :]) for val in clustDataK)/len(indexK)
                        __Bji = min( __Bji, __Dki)

            SSWC_value += (__Bji - __Aji) / max(__Bji ,__Aji)
        
    return SSWC_value / len(X)
        

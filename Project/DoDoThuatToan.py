import math
import numpy as np

###
''' Do Do Thuat Toan DB '''
###
def DB(data, center, numClust, U):
    def d( X1, l, m):
        return np.linalg.norm(X1[l] - X1[m])

    def d1( X, X1, U, l):
        sum1 = 0
        for Xi in U[:, l]:
            sum1 += np.linalg.norm(Xi - X1[l])
            
        return sum1/N[l]

    def D(X, X1, U, C, l, m):
        N = len(X)
        __Tu = d1( X, X1, C, l) + d1( X, X1, C, m)
        __Mau = d( X1, l, m)
        return __Tu / __Mau

    sum1 = 0
    for j in range(numClust):
        listD = list()
        for l in range(j):
            for m in range(j):
                if ( l != m):
                    listD.append(D(data, center, numClust, U, l, m))

        sum1 += max(listD) if len(listD) > 0 else 0

    return sum1/numClust

###
''' Do Do Thuat Toan IFV '''
###
def IFV( X, V, C, U):
    U = np.array(U)
    eps = 0.01
    def SDmax(V, j):
        listSD = list()
        for k in range(j):
            for i in range(j):
               if(i != k):
                  listSD.append(pow(np.linalg.norm(V[k] - V[i]), 2))
                  
        return max(listSD) if len(listSD) > 0 else 0
    
    def Sigma1D(X, V, C, N):
        sum1 = 0;
        for j in range(C):
            sum2 = 0
            for k in range(N):
                sum2 += pow(np.linalg.norm(X[k] - V[j]), 2)
            sum1 += sum2/N
        return sum1/C

    N = len(X)
    sum1 = 0
    for j in range(C):
        sum2 = 0
        for k in range(N):
            sum3 = 0
            for k in range(N):
                if U[k, j] == float(0):
                    U[k, j] = eps
                    
                if U[k, j] == float(1):
                    U[k, j] = 1 - eps
                sum3 += math.log(U[k, j], 2)
            sum2 += pow(U[k, j], 2) * pow(math.log(C, 2) - sum3/N, 2)

        __TuSo = SDmax(V, j)
        __MauSo = Sigma1D(X, V, C, len(X))
        sum1 += sum2/N*__TuSo/__MauSo

    return sum1/C

###
''' Do Do Thuat Toan PDM '''
###
def PDM( X, X1, k, U ):
    N = len(X)
    def E1():
        sum1 = 0
        for i in range(N):
            sum1 += np.linalg.norm(X[i] - X1)
        return sum1

    def Ek():
        sum1 = 0
        for l in range(k):
            for Xi in U[:, l]:
                sum1 += np.linalg.norm(Xi - X1[l])
        return sum1

    def Dk():
        list1 = list()
        for l in range(k):
            for m in range(k):
                list1.append(np.linalg.norm(X1[l] - X1[m]))
        return max(list1)

    __E1 = E1()
    __Ek = Ek()
    __Dk = Dk()
    return pow( __E1*__Dk/__Ek/k, 2)

###
''' Do Do Thuat Toan SSWC '''
###
def SSWC(X, X1, C, U):
    maxU = max(np.unique(U))
    SSWC_value = 0
    for j in range(C):
        index = np.where(U[:, j] == maxU)[0]
        clustData = X[index, :]
        for i in index:
            __Aji = sum(np.linalg.norm(val - X[i, :]) for val in clustData)/len(index)
            __Bji = 10^6

            for k in range(C):
                if k != j :
                    indexK = np.where(U[:, k] == maxU)[0]
                    clustDataK = X[indexK, :]
                    __Dki = sum(np.linalg.norm(val - X[i, :]) for val in clustDataK)/len(indexK)
                    __Bji = min( __Bji, __Dki)

            SSWC_value += (__Bji - __Aji) / max(__Bji ,__Aji)
        
    return SSWC_value / len(X)
        

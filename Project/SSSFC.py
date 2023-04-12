import numpy as np
import pandas as pd
import math 

def randomV(X, uNgang, C):
    __AllV = list()
    for i in range(C):
        __V = list()
        for j in range(X.shape[-1]):
            __V.append(sum(uNgang[:, i] * X[:, j]))
        __AllV.append(__V)
    return __AllV

def sigma(start, end, functionHandle ):
    result = 0
    for i in range(start, end + 1):
        result += functionHandle(i)
    return result

# Khoang Cach
def distance(X, V):
    return math.dist(X, V)

def ArgMin(X, V, k):
    __allKhoangCach = np.array([])
    for i in range(len(V)):
        __KhoangCach = distance(X[k], V[i])
        __allKhoangCach = np.append(__allKhoangCach, __KhoangCach)
    return np.argmin(__allKhoangCach)

def U( X, V, uNgang, m, k, j):
    result = uNgang[k, j]

    if (X[k] in V):
        return result
    
    if(m == 1):
        if( k == ArgMin(X, V, k)) :
            result += 1 - sum(uNgang[k, : len(V)])
    else:
        __Tu = pow((1.0 / distance(X[k], V[j])), 2/(m-1))
        __Mau = sum(pow(1.0 / distance(X[k], V[i]), 2/(m-1)) for i in range(len(V)))

        if(__Mau != 0):
            result += (1 - sum(uNgang[k, : len(V)])) * __Tu / __Mau
    return result

def arrU(X, V, uNgang, m):
    __U = np.array(np.ones(shape=(len(X), len(V))))
    for k in range(len(X)):
        for j in range(len(V)):
            __U[k, j] = U( X, V, uNgang, m, k, j)
    return __U

def V( X, __U, __UNgang, m, j):

    d = list()
    for i in range(X.shape[-1]):
        d.append(pow(abs(__U[:, j]-__UNgang[:, j]), m))
    
    __Tu = sum(np.array(d).T*X)
    __Mau = sum(pow(abs(__U[:, j]-__UNgang[:, j]), m))
    return __Tu/__Mau

def allV( X, __U, __UNgang, m, C):
    __V = np.array(np.ones(shape=(C, np.array(X).shape[-1])))
    for j in range(0, C):
        __V[j] = V(X, __U, __UNgang, m, j)
    return __V

def checkDistanceV(V1, V2, e):
    for i in range(max(len(V1), len(V2))):
        if(distance(V1[i], V2[i]) <= e):
            return True
    return False

def SSSFC(X, uNgang, m, C, nguong = pow(10, -6), maxStep = 100000):
    N = X.shape[0]
    t = 0
    V = np.array([randomV(X, uNgang, C)])

    while(t <= maxStep):
        t += 1
        __U = arrU(X, V[-1], uNgang, m)
        __V = allV( X, __U, uNgang, m, C)
        if(checkDistanceV(V[-1], __V, nguong)):
            break;
        V = np.concatenate((V, np.array([__V])))
        print("V thu ", len(V), " : ")
        print(V[-1])

    print("V cuoi cung : ")
    print(V[-1])

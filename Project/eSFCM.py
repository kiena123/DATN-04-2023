import numpy as np
import math
import pandas as pd

arrNhap = np.array([ 1, 2, 3])
__Lambda = 1
e = math.exp(1)
# U1 : Ungang

def initV1( X, U1, C):
    N, r = X.shape
    V = np.zeros(shape = (C, r))
    for j in range(C):
        for i in range(r):
            __TuSo = 0
            __MauSo = 0
            for k in range(N):
                __TuSo += X[k, i] * pow(U1[k, j], 2) 
                __MauSo += pow(U1[k, j], 2)
            V[j, i] = __TuSo/__MauSo if __MauSo != 0 else 0 

    return np.array(V)

def initA( X, V, U1):
    N, r = X.shape
    sum1 = 0
    
    for j in range(len(V)):
        for k in range(N):
            sum1 += pow(U1[k, j], 2) * (X[k] - V[j]) * (X[k] - V[j]).T

    P = sum1/N

    return 1/P

def dA( A, x1, x2):
    __Hieu = x1 - x2
    return pow(__Hieu.T * A * __Hieu, 1/2)
    
def initU(X, V, U1):
    __U =  list()
    __A = initA(X, V, U1)
    print(__A)
    for k in range(len(X)):
        __Uk = list()
        for j in range(len(V)):
            __Tu = pow( e, -__Lambda * dA(__A, X[k], V[j]))
            __Mau = 0
            __sumU1 = 0
            for i in range(len(V)):
                __Mau += pow( e, -__Lambda * dA(__A, X[k], V[i]))
                __sumU1 += U1[k][i]
            __Uk.append(U1[k, j] + ((1 - __sumU1)*__Tu/__Mau))
        __U.append(__Uk)
    return np.array(__U)

def initV(X, U, C):
    __V = list()
    for j in range(C):
        __Tu = 0
        __Mau = 0
        for k in range(len(X)):
            __Tu += X[k] * U[k, j]
            __Mau += U[k, j]
        __V.append(__Tu/__Mau)
    return np.array(__V)

def initJ(X, V, U, A, U1):
    __Sum1 = 0
    __Sum2 = 0
    for k in range(len(X)):
        for j in range(len(V)):
            __Sum1 += U[k, j] * dA( A, X[k], V[j])
            __UngangU = abs(U[k, j] - U1[k, j])
            __Sum2 += __UngangU * math.ln(__UngangU)
    return min(__Sum1 + pow(__Lambda, -1) * __Sum2)

def checkDistanceV(V1, V2, nguong):
    for i in range(max(len(V1), len(V2))):
        if(np.linalg.norm(V1[i] - V2[i]) <= nguong):
            return True
    return False

def ESFCM(X, U1, C, m, eps = 0.001, maxStep = 1000, lamda = 1):
    t = 1
    arrV = np.array([initV1(X, U1, C)])
    __U = U1
    while(t <= maxStep):
        t += 1
        __U = initU(X, arrV[-1], __U)
        __V = initV( X, __U, C)
        if(checkDistanceV(arrV[-1], __V, eps)):
            break;
        arrV = np.concatenate((arrV, np.array([__V])))
        print("V thu ", len(arrV))
        
    for i in range(len(arrV)):
        print(arrV[i])
    print("End")
    
def main():
    X = np.array(pd.read_csv('./Data/Test/X.csv', header=None))
    Ungang = np.array(pd.read_csv('./Data/Test/UNgang.csv', header=None)).T
    C = 3
    m = 2
    ESFCM(X, Ungang, C, m, eps = 0.000001)

main()

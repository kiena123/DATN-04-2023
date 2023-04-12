import numpy as np
import math
import pandas as pd

arrNhap = np.array([ 1, 2, 3])
__Lambda = 1
# exp
e = math.exp(1)
# U1 : Ungang

def initV( X, U1, C):
    V = list()
    for j in range(C):
        __Tu = 0
        __Mau = 0
        for k in range(len(X)):
            __Tu += X[k] * pow(U1[k, j], 2)
            __Mau += pow(U1[k, j], 2)
        V.append(__Tu/__Mau)
    return np.array(V)

def A( X, V, U1):
    __A = 0
    for j in range(len(V)):
        for k in range(len(X)):
            __Hieu = X[k] - V[j]
            __A += pow(U1[k, j], 2) * __Hieu * __Hieu.T
    return __A/len(X)

def dA( A, x1, x2):
    __Hieu = x1 - x2
    return pow(__Hieu.T * A * __Hieu, 1/2)

def Ukj( X, V, A, U1, k, j):
    __sumU1 = 0
    __Tu = pow( e, -__Lambda * dA(A, X[k], V[j]))
    # __Tu = math.exp(-__Lambda * dA(A, X[k], V[j]))
    __Mau = 0
    for i in range(len(V)):
        __Mau += pow( e, -__Lambda * dA(A, X[k], V[i]))
        # __Mau += math.exp(-__Lambda * dA(A, X[k], V[i]))
        __sumU1 += U1[k][i]

    return U1[k, j] + ((1 - __sumU1)*__Tu/__Mau)
    
def U(X, V, U1):
    __U =  list()
    __A = A(X, V, U1)
    for k in range(len(X)):
        __Uk = list()
        for j in range(len(V)):
            __Uk.append(Ukj(X, V, __A, U1, k, j))
        __U.append(__Uk)
    return np.array(__U)

def Vj( X, U, C, j):
    __Tu = 0
    __Mau = 0
    for k in range(len(X)):
        __Tu += X[k] * U[k, j]
        __Mau += U[k, j]
    return __Tu/__Mau

def V(X, U, C):
    __V = list()
    for j in range(C):
        __V.append(Vj( X, U, C, j))
    return np.array(__V)

def J(X, V, U, A, U1):
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
        if(math.dist(V1[i], V2[i]) <= nguong):
            return True
    return False

def ESFCM(X, U1, C, m, Eps = 0.001, maxStep = 1000, lamda = 1):
    t = 1
    arrV = np.array([initV(X, U1, C)])

    while(t <= maxStep):
        t += 1
        __U = U(X, arrV[-1], U1)
        __V = V( X, __U, C)
        if(checkDistanceV(arrV[-1], __V, Eps)):
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
    ESFCM(X, Ungang, C, m)

main()

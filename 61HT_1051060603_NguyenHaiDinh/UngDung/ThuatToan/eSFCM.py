from PIL import Image
import numpy as np
import math
import pandas as pd


arrNhap = np.array([ 1, 2, 3])
e = math.exp(1)
# U1 : Ungang


def eSFCM(X, U1, C, m, eps = 0.001, maxStep = 1000, lamda = 0.000001):
    def initV1( X, C):
        N, r = X.shape
        print("Lamda : ", lamda)
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

    def initA(X, V):
        N, r = X.shape
        sum1 = 0
        
        for j in range(len(V)):
            for k in range(N):
                # print(pow(U1[k, j], 2) * np.matmul((X[k] - V[j]) ,(X[k] - V[j]).T))
                __Hieu = X[k] - V[j]
                sum1 += pow(U1[k, j], 2) * np.matmul( __Hieu,__Hieu.T)
        P = sum1/N
        
        return P

    def dA( A, x1, x2):
        __Hieu = x1 - x2
        result = np.matmul(__Hieu.T, __Hieu) * A
        return result
        
    def initU(X, V, A):
        N, r = X.shape
        newU = np.zeros(shape = U1.shape)
        __A = A
        for k in range(len(X)):
            for j in range(len(V)):
                __Tu = math.exp(-lamda * dA(__A, X[k], V[j]))
                __Mau = 0
                __sumU1 = 0
                for i in range(len(V)):
                    __Mau += math.exp(-lamda * dA(__A, X[k], V[i]))
                    __sumU1 += U1[k, i]

                if __Mau != 0 :
                    newU[k, j] = U1[k, j] + (1 - __sumU1)*__Tu/__Mau
                else :
                    newU[k, j] = U1[k, j]

        return np.array(newU)

    def initV(X, U, C):
        N, r = X.shape
        newV = np.zeros(shape = (C, r))
        for j in range(C):
            for i in range(r):
                __Tu = 0
                __Mau = 0
                for k in range(N):
                    __Tu += X[k, i] * U[k, j]
                    __Mau += U[k, j]
                
                if __Mau != 0:
                    newV[j, i] = __Tu/__Mau
        return np.array(newV)

    def initJ(X, V, U):
        __Sum1 = 0
        __Sum2 = 0
        __A = initA(X, V, U1)
        for k in range(len(X)):
            for j in range(len(V)):
                __Sum1 += U[k, j] * dA( __A, X[k], V[j])
                __UngangU = np.linalg.norm(U[k, j] - U1[k, j])
                if __UngangU != 0:
                    __Sum2 += __UngangU * math.log(__UngangU)
        return (__Sum1 + pow(lamda, -1) * __Sum2)
        
    t = 0
    V = initV1(X, C)
    U = np.array(U1)
    A = initA(X, V)
    print(V)
    while(t <= maxStep):
        t += 1
        print("Lap thu ", t)
        __U = initU(X, V, A)
        __V = initV( X, __U, C)
        '''
        
        if(np.linalg.norm(V - __V) <= eps):
        
        '''
        print(np.linalg.norm(V - __V))
        print(np.linalg.norm(U - __U))
        if(np.linalg.norm(U - __U) <= eps):
            break;
        V = __V
        U = __U
    
    print("End")
    # 
    return U, V
    
def main():
    imageInput = np.array(Image.open("./Result/inputImage.png"))
    X = imageInput.reshape((imageInput.shape[0]*imageInput.shape[1], imageInput.shape[-1]))
    Ungang = np.array(pd.read_csv("./Result/U1.csv", header = None), dtype = int)
    C = 2
    m = 2
    U, V = eSFCM(X, Ungang, C, m, eps = 0.000001)
    print(U)
    print(V)


# main()





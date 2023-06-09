from PIL import Image
import numpy as np
import pandas as pd
import math 

def SSSFC(X, uNgang, C = 2, m = 2, eps = 0.01, maxStep = 150):
    limit = 3
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
                # V[j, i] = round(__TuSo/__MauSo, limit) if __MauSo != 0 else 0
                V[j, i] = __TuSo/__MauSo if __MauSo != 0 else 0
                
        return np.array(V)

    def initU( X, V, U1, m):
        N, r = X.shape
        C = len(V)
        newU = np.zeros(shape=U1.shape, dtype = float)

        for k in range(N):
            for j in range(C):
                if m == 1 :  
                    if k == np.argmin(np.linalg.norm(X[k] - V[i]) for i in range(C)):
                        sum1 = 0
                        for i in range(C):
                            sum1 += U1[k, i]
                            
                        # newU[k, j] = round(U1[k, j] + 1 - sum1, limit)
                        newU[k, j] = U1[k, j] + 1 - sum1
                    else :
                        # newU[k, j] = round(U1[k, j] , limit)
                        newU[k, j] = U1[k, j]
                else :
                    sum1 = 0
                    sum2 = np.linalg.norm(X[k] - V[j])
                    if(sum2 != 0):
                        sum2 = pow(1/sum2, 2/(m-1))
                    else :
                        sum2 = 0
                    
                    sum3 = 0
                    for i in range(C):
                        sum1 += U1[k, i]
                        __Mauso = np.linalg.norm(X[k] - V[i])
                        if __Mauso != 0:
                            sum3 += pow(1/__Mauso, 2/(m-1))
                    
                    sum1 = 1 - sum1

                    if sum3 != 0:
                        # newU[k, j] = round(U1[k, j] + sum1 * sum2 / sum3 , limit)
                        newU[k, j] = U1[k, j] + sum1 * sum2 / sum3
                    else :
                        # newU[k, j] = round(U1[k, j] , limit)
                        newU[k, j] = U1[k, j]
                                
        return np.array(newU)

    def initV( X, U, U1, m, C):
        N, r = X.shape
        newV = np.zeros(shape=(C, r))
        for j in range(C):
            for i in range(r):
                __Tu = 0
                __Mau = 0
                for k in range(N):
                    __Tu +=  pow(abs(U[k, j] - U1[k, j]), m) * X[k, i]
                    __Mau += pow(abs(U[k, j] - U1[k, j]), m)
                
                if __Mau != 0:
                    # newV[j, i] = round(__Tu/__Mau, limit)
                    newV[j, i] = __Tu/__Mau

        return np.array(newV)

    def initJ(X, V, U):
        N, r = X.shape
        C = len(V)
        __J = 0
        for k in range(N):
            for j in range(C):
                __J += pow(abs(U[k, j] - U1[k, j]), m) * pow(np.linalg.norm(X[k] - V[j]), 2)
        return __J

    print("Bat dau voi SSSFC ")
    N = X.shape[0]
    t = 0
    V = initV1(X, uNgang, C)
    U = 0
    while(t <= maxStep):
        print("Chay lan ", t)
        t += 1
        print(V)
        __U = initU(X, V, uNgang, m)
        __V = initV( X, __U, uNgang, m, C)
        '''
        print(np.linalg.norm(U - __U))
        if(np.linalg.norm(U - __U) <= eps):
        '''
        print(np.linalg.norm(V - __V))
        if(np.linalg.norm(V - __V) <= eps):
            break
        else :
            U = __U
            V = __V

    return (U, np.array(V))

# Test
def main():
    imageInput = np.array(Image.open("./Result/inputImage.png"))
    X = imageInput.reshape((imageInput.shape[0]*imageInput.shape[1], imageInput.shape[-1]))
    Ungang = np.array(pd.read_csv("./Result/U1.csv", header = None), dtype = int)
    C = 2
    m = 3
    U, V = SSSFC(X, Ungang, C, m, eps = 0.000001)
    print(U)
    print(V)

# main()

from PIL import Image
import numpy as np
import pandas as pd

#   FCM
def FCM(X,C,m = 2,Eps = 0.001,maxStep = 200):
    def randomU(X):
        __U = list()
        for k in range(len(X)):
            __U.append(np.random.dirichlet(np.ones(C),size=1)[0])
        return np.array(__U)
    
    def initU( X, V, m):
        __U = np.zeros(shape=(len(X), len(V)))
        for k in range(len(X)):
            for j in range(len(V)):
                sum1 = 0
                __Tu = np.linalg.norm(X[k] - V[j])
                for i in range(C):
                    __Mau = np.linalg.norm(X[k] - V[i])
                    sum1 += pow(__Tu/__Mau, 1/(m - 1))
                __U[k, j] = 1/sum1
        return __U

    def initV( X, U, C, m):
        N, r = X.shape
        __V = list()
        for j in range(C):
            sum1 = 0
            sum2 = 0
            for k in range(N):
                sum1 += pow(U[k, j], m) * X[k]
                sum2 += pow(U[k, j], m)
            __V.append(sum1/sum2)
        return np.array(__V)

    def initJ(X, V, U):
        sum1 = 0
        for k in range(len(X)):
            for j in range(len(V)):
                sum1 += pow( U[k, j], m) * pow( np.linalg.norm( X[k] - V[j]), 2)

        return sum1

    t = 0
    U = randomU(X)
    V = np.zeros
    
    while(t <= maxStep):
        t += 1
        V = initV( X, U, C, m)
        __U = initU( X, V, m)
        if(np.linalg.norm( __U - U).all() <= Eps):
            break;
        U = __U

    return [ U, V, initJ(X, V, U)]


#   SSFCMBP
def SSFCMBP(X, U1, C, m = 2, Eps = 0.0001, maxStep = 200):
    N, r = X.shape
    H = 2
    Beta = 0.06
    Alpha = 1
    # [U, V, J] = FCM(X,C,m = 2,Eps = 0.001,maxStep = 200)
    # la gia tri cua ki hieu delta 
    B= np.ones(shape=(N,1))
    maxU1 = max(np.unique(U1))

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
    
    def initL( U1, H, N, C):
        L = np.zeros(shape=(N, 1)).astype(int)
        for k in range(N):
            for j in range(C):
                if U1[k, j] == maxU1:
                    L[k] = j
        return L

    def initH1(L, N, C):
        H1 = np.zeros(shape=(N, 1)).astype(int)
        for k in range(N):
            if L[k] == 1:
                H1[k] = 1
            else :
                H1[k] = 2
        return H1
                
    def initF(H1, H, N):
        # F do thuoc bo tro cua diem du lieu -> lop nao
        F = np.zeros(shape=(N, H)).astype(int)
        for i in range(H):
            for k in range(N):
                if(H1[k] == i):
                    F[k, i] == 1
        return F

    def initPi(H1, L, H, N, C):
        Pi = np.zeros(shape=(C, H)).astype(int)
        for h in range(H):
            for j in range(C):
                for k in range(N):
                    if(H1[k] == h and L[k] == j):
                        Pi[j,h]=j;
        return Pi

    def initM(Pi, H, C):
        # M do thuoc bo tro cua cumf -> lop nao
        M = np.zeros(shape=(C, H)).astype(int)
        for h in range(H):
            for j in range(C):
                if Pi[j, h] == j:
                    M[j, h] == 1;
                else :
                    M[j, h] == 0;
        return M

    def D( x1, x2):
        return np.linalg.norm(x1 - x2)

    def initU1( U1, L, Pi, F, H, N, C):
        newU1 = np.zeros(shape = U1.shape)
        
        for k in range(N):
            for j in range(C):
                sum1 = 0
                for h in range(H):
                    sum2 = 0
                    for i in range(C):
                        if Pi[i, h] == i:
                            sum2 += U1[k, i]
                    for i in range(C):
                        if Pi[i, h] == L[k]:
                            sum1 += F[k, h] - sum2
                            break
                newU1[k, j] = 2 * U1[k, j] * Beta * B[k] * sum1
                    
        return newU1

    def initU( X, V, U1):
        N, r = X.shape
        C = len(V)
        __U = np.zeros(shape = (N, C))
        for k in range(N):
            for j in range(C):
                sum1 = 0
                # sum2 = 0.000001
                sum2 = 0
                for l in range(C):
                    sum1 += U1[k, l]
                    if D(X[k], V[l]) != 0:
                        sum2 += D(X[k], V[j])/D(X[k], V[l])

                __Bien1 = Alpha/(1 + Alpha)

                if sum2 != 0:
                    __U[k, j] = __Bien1 * U1[k, j] + (1 - __Bien1*sum1)/sum2
                else :
                    __U[k, j] = __Bien1 * U1[k, j]
        return __U

    def initV(X, U, U1, C):
        __V = list()
        for j in range(C):
            __Tu = 0
            __Mau = 0
            for k in range(len(X)):
                __Tu += pow(U[k, j], 2) + Alpha * pow(U[k, j] - U1[k, j], 2) * X[k]
                __Mau += pow(U[k, j], 2) + Alpha * pow(U[k, j] - U1[k, j], 2)
            __V.append(__Tu/__Mau)

        return np.array(__V)
            

    def initLamda( X, V, U1):
        N = len(X)
        C = len(V)
        sum1 = 0
        sum2 = 0
        for k in range(N):
            for j in range(C):
                sum1 += U1[k, j]
                sum2 += 1/(2 * (1 + Alpha) * pow(D(X[k], V[j]),2))

        __Tu = 1 - Alpha*sum1/(1 + Alpha)
        return __Tu / sum2

    def initJ( X, V, U, U1):
        lamda = initLamda( X, V, U1)
        N = len(X)
        C = len(V)
        sum1 = 0
        sum2 = 0
        sum3 = 0
        for j in range(C):
            for k in range(N):
                sum1 += pow(U[k, j], 2) * pow( D(X[k], V[j]), 2)
                sum2 += pow(U[k, j] - U1[k, j], 2) * pow(D(X[k], V[j]), 2) * B[k]
                sum3 += U[k, j] - 1

        return sum1 + Alpha * sum2 + lamda * sum3
    ####

    L = initL(U1, H, N, C)        # Danh sach tam cua diem du lieu
    H1 = initH1(L, N, C)       # Danh sach lop cua diem du lieu
    F = initF(H1, H, N)
    Pi = initPi(H1, L, H, N, C)
    M = initM(Pi, H, C)
    t = 0
    V = initV1( X, U1, C)
    U = initU( X, V, U1)
    while(t <= maxStep):
        t += 1
        print("Lan ", t)
        '''
        while(1 > 0):
            print("Duyet U1")
            __U1 = initU1(U1, L, Pi, F, H, N, C)
            print(np.unique(__U1))
            if(D(__U1, U1) <= Eps):
                break;
            else:
                U1 = __U1
        '''
        while(1 > 0):
            __V = initV(X, U, U1, C)
            __U = initU( X, __V, U1)
            print("Dist __V va V", np.linalg.norm(V - __V))
            if(np.linalg.norm(V - __V) <= Eps):
                break;
            V = __V
            U = __U

        print("Gan lai M")
        maxU1 = max(np.unique(U1))
        L = initL(U1, H, N, C)
        Pi = initPi(H1, L, H, N, C)
        __M = initM(Pi, H, C)

        if(M.all() == __M.all()):
            break;
        else :
            M = __M
    print(U1)
    print("------")
    return (U, V)

def main():
    '''
    X = np.array(pd.read_csv('./Data/Test/X.csv', header=None))
    Ungang = np.array(pd.read_csv('./Data/Test/UNgang.csv', header=None)).T
    C = 3
    m = 2
    '''
    #'''
    imageInput = np.array(Image.open("./Result/inputImage.png"))
    X = imageInput.reshape((imageInput.shape[0]*imageInput.shape[1], imageInput.shape[-1]))
    # print(X)
    Ungang = np.array(pd.read_csv("./Result/U1.csv", header = None), dtype = int)
    # print(Ungang)
    C = 2
    m = 2
    #'''
    U, V = SSFCMBP( X, Ungang, C, m, 0.01, 150)
    print("U : ")
    print(U)
    print("V : ")
    print(V)
    
# main()

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
    [U, V, J] = FCM(X,C,m = 2,Eps = 0.001,maxStep = 200)
    # la gia tri cua ki hieu delta 
    B= np.ones(shape=(N,1))
    
    def initL( U1, H, N, C):
        L = np.zeros(shape=(N, 1)).astype(int)
        for k in range(N):
            for j in range(C):
                if U1[k, j] == 1:
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
        newU1 = U1
        for k in range(N):
            for j in range(C):
                if(L[k] in Pi[j]) :
                    newU1[k, j] += 2 * Beta * B[k] * sum( F[k, h] - sum(U1[k, i] for i in Pi[:, h].astype(int)) for h in range(H))
        
        return newU1

    def initU( X, V, U1):
        N = len(X)
        C = len(V)
        __U = np.zeros(shape = (N, C))
        for k in range(N):
            for j in range(C):
                sum1 = 0
                sum2 = 0
                for l in range(C):
                    sum1 += U1[k, l]
                    sum2 += D(X[k], V[j])/D(X[k], V[l])

                __Bien1 = Alpha/(1 + Alpha)
                __U[k, j] = __Bien1 * U1[k, j] + (1 - __Bien1*sum1)/sum2

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

    def initJ( X, V, U, U1, lamda):
        N = len(X)
        C = len(V)
        sum1 = 0
        sum2 = 0
        sum3 = 0
        for j in range(C):
            for k in range(N):
                sum1 += pow(U[k, j], 2) * pow( D(X[k], V[j]), 2)

            for k in range(L):
                sum2 += pow(U[k, j] - U1[k, j], 2) * pow(D(X[k], V[j]), 2)

            sum3 += U[k, j] - 1

        return sum1 + Alpha * sum2 + lamda * sum3
    ####

    L = initL(U1, H, N, C)        # Danh sach tam cua diem du lieu
    H1 = initH1(L, N, C)       # Danh sach lop cua diem du lieu
    F = initF(H1, H, N)
    Pi = initPi(H1, L, H, N, C)
    M = initM(Pi, H, C)
    t = 0
    while(t <= maxStep):
        t += 1
        print("Lan ", t)
        while(1 > 0):
            __U1 = initU1(U1, L, Pi, F, H, N, C)
            if(D(__U1, U1) <= Eps):
                break;
            U1 = __U1
        while(1 > 0):
            __V = initV(X, U, U1, C)
            __U = initU( X, __V, U1)
            if(D(__U, U) <= Eps):
                break;
            V = __V
            U = __U
        L = initL(U1, H, N, C)
        Pi = initPi(H1, L, H, N, C)
        __M = initM(Pi, H, C)

        if(M.all() == __M.all()):
            break;
        else :
            M = __M

    print("V : ")
    print(V)

def main():
    X = np.array(pd.read_csv('./Data/Test/X.csv', header=None))
    Ungang = np.array(pd.read_csv('./Data/Test/UNgang.csv', header=None)).T
    C = 3
    m = 2
    SSFCMBP( X, Ungang, C, m, 0.01, 150)

main()

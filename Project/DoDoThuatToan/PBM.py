import numpy as np 


def PDM( X, X1, k ):
    def E1():
        sum1 = 0
        for i in range(N)
            sum1 += np.linalg.norm(X[i] - X1)
        return sum1

    def Ek():
        sum1 = 0
        for l in range(k):
            for Xi in C[l]:
                sum1 += np.linalg.norm(Xi - X1[l])
        return sum1

    def Dk():
        __max
        for l in range(k):
            for m in range(k):
               if(__max = null):
                   __max = np.linalg.norm(X1[l] - X1[m])
                else :
                    if __max < np.linalg.norm(X1[l] - X1[m]) :
                    __max = np.linalg.norm(X1[l] - X1[m])
        return __max

    __E1 = E1()
    __Ek = Ek()
    __Dk = Dk()
    return pow( __E1*__Dk/__Ek/k, 2)

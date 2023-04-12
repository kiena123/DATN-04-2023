

import numpy as np
import pandas as pd

def distance( x1, x2 ):
    maxRange = max(len(x1), len(x2))
    sumPow = 0
    for i in range(maxRange):
        sumPow += pow((x1[i]) - x2[i], 2)
    return np.sqrt(sumPow)

def cdist( X, centers):
    result = []
    

    
def kmean_init_centers( X, k):
    tbc = int(len(X)/(k-1))
    arr = []

    for i in range(k):
        arr.append(X[i*tbc,:])
    
    return np.array(arr)

def kmean_assign_labels( X, centers):
    
    return     

if __name__ == "__main__":
    url = "./weatherSunRain.csv"
    X = np.array(pd.read_csv(url))
    k = 3

    print(distance([1,1], [2, 2]))

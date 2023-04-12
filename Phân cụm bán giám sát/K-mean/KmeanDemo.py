#    Chu y:
#        - Phai install scipy



from __future__ import print_function 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

# khoi tao cac center ban dau
def kmeans_init_centers(X, k):
    arr = []
    for i in range(k):
        arr.append(X[i*100])

    # randomly pick k rows of X as initial centers
    # return X[np.random.choice(X.shape[0], k, replace=False)]
    return np.array(arr)

# gan nhan moi cho cac diem khi biet center
def kmeans_assign_labels(X, centers):
    # calculate pairwise distances btw data and centers
    # CT : distance = np.sqrt(pow(X1 - X2, 2) + pow(Y1 - Y2, 2))
    D = cdist(X, centers)
    # return index of the closest center
    return np.argmin(D, axis = 1)

# cap nhat cac center moi theo du lieu vua duoc gan nhan 
def kmeans_update_centers(X, labels, K):
    centers = np.zeros((K, X.shape[1]))
    for k in range(K):
        # collect all points assigned to the k-th cluster 
        Xk = X[labels == k, :]
        # take average
        centers[k,:] = np.mean(Xk, axis = 0)
    return centers

# kiem tra dieu kien dung cua thuat toan
def has_converged(centers, new_centers):
    # return True if two sets of centers are the same
    return (set([tuple(a) for a in centers]) == 
        set([tuple(a) for a in new_centers]))

# phan chinh
def kmeans(X, K):
    centers = [kmeans_init_centers(X, K)]
    labels = []
    it = 0 
    while True:
        labels.append(kmeans_assign_labels(X, centers[-1]))
        new_centers = kmeans_update_centers(X, labels[-1], K)
        if has_converged(centers[-1], new_centers):
            break
        centers.append(new_centers)
        it += 1
    return (centers, labels, it)


def predict_kmeans(X, centers):
    indexCenters = 0
    dist = distance(X, centers[0])

    for i in range(1, len(centers)):
        if ( dist > distance(X, centers[i])):
            indexCenters = i
            dist = distance(X, centers[i])
   
    return indexCenters

def distance( x1, x2 ):
    return np.sqrt(pow(x1[0][0] - x2[0], 2) + pow(x1[0][1] - x2[1], 2)) 

# Bai lam :
if __name__ == "__main__":
    url = "./weatherSunRain.csv"
    # url = "D:/DHTL/Nam 4-1/Khai-pha-du-lieu/dataEdited.csv"
    X = pd.read_csv(url)
    
    if 'weather' in X.keys() :
        del X['weather']
    
    K = 2
    N = (int)(len(X) / K)

    X = np.array(X)

    (centers, labels, it) = kmeans(X, K)
    print(labels)
    print('Centers found by our algorithm:')
    print(centers[-1])

    

from DoDoThuatToan import *
from SSSFC import SSSFC
#
import numpy as np
import pandas as pd

X = np.array(pd.read_csv('./Data/Test/X.csv', header=None))
U1 = np.array(pd.read_csv('./Data/Test/UNgang.csv', header=None)).T
C = 3
m = 2

U, V, J = SSSFC(X, U1, m, C, nguong = 0.001)

print("DB")
# print(DB(X, V, C, U))
print("IFV")
print(IFV(X, V, C, U))
print("PDM")
print(PDM(X, V, C, U))
print("SSWC")
print(SSWC(X, V, C, U))


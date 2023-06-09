from PIL import Image
from DoDoThuatToan import *
from SSSFC import SSSFC
from eSFCM import eSFCM
from SSFCMBP import SSFCMBP
#
import numpy as np
import pandas as pd

'''
X = np.array(pd.read_csv('./Data/Test/X.csv', header=None))
U1 = np.array(pd.read_csv('./Data/Test/UNgang.csv', header=None)).T
C = 3
m = 2
'''

imageInput = np.array(Image.open("./Result/inputImage.png"))
X = imageInput.reshape((imageInput.shape[0]*imageInput.shape[1], imageInput.shape[-1]))
U1 = np.array(pd.read_csv("./Result/U1.csv", header = None), dtype = int)
C = 2
m = 2
# U, V = SSSFC(X, U1, C, m, 0.001)
U, V = eSFCM(X, U1, C, m, 0.001)
# U, V = SSFCMBP(X, U1, C, m, 0.001)

print("DB")
print(DB(X, V, C, U))
print("IFV")
print(IFV(X, V, C, U))
print("PDM")
print(PDM(X, V, C, U))
print("SSWC")
print(SSWC(X, V, C, U))


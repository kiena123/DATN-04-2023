from PIL import Image
from DoDoThuatToan import *
from SSSFC import SSSFC
from eSFCM import eSFCM
from SSFCMBP import SSFCMBP
#
import numpy as np
import pandas as pd

imageInput = np.array(Image.open("./Img/5.jpg"))
X = imageInput.reshape((imageInput.shape[0]*imageInput.shape[1], imageInput.shape[-1]))
U1 = np.array(pd.read_csv("./Img/5.csv", header = None), dtype = int)
C = 2
m = 1.5

U, V = SSSFC(X, U1, C, m, 0.001)
# U, V = eSFCM(X, U1, C, m, 0.001, 150, 4)
# U, V = SSFCMBP(X, U1, C, m, 0.001)

print(U)
print("----------------------")
print(V)

print("DB")
print(DB(X, V, C, U))
print("IFV")
print(IFV(X, V, C, U))
print("PDM")
print(PDM(X, V, C, U))


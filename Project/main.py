import numpy as np
import pandas as pd
import cv2
from PIL import Image
from SSSFC import SSSFC

# SSSFC
def initUNgang(img, sURLData, sURLCluster, C):
    sizeImg = img.size
    __Clusters = set()
    __UNgang = pd.DataFrame(np.zeros( shape = (sizeImg[0]*sizeImg[1], C)))

    
    for i in np.loadtxt(sURLData):
        __Dot = list([ round(i[1]*sizeImg[0]), round(i[2]*sizeImg[1])])
        __Khung = list([ round(i[3]*sizeImg[0]), round(i[4]*sizeImg[1])])
        start = (__Dot[1]-1)*sizeImg[0] + __Dot[0]
        for j in range(0, __Khung[1]):
            numNow = start + (sizeImg[0] * j)
            listNum = str(list(range(numNow, numNow + __Khung[0] + 1)))[1:-1].split(",")
            __UNgang.loc[ range(numNow, numNow + __Khung[0] + 1), int(i[0])] = float(i[0])


    print("Da luu U ngang")
    __UNgang.to_csv(f"{saveFolder}/UNgang.csv", index = False, mode="w")
    return np.array(__UNgang)

def HandleData(urlImg):
    # Tạo ảnh background trắng
    img = Image.open(urlImg).convert("RGBA")
    bg = Image.new("RGBA", img.size, (255, 255, 255))
    bg.paste(img, list((0, 0) + img.size), img)
    bg.save(f'{saveFolder}/result.png', format = "png")
    # Convert ảnh (2) từ brg sang gray (search opencv convert to gray)
    image = cv2.imread(urlImg)
    # cv2.imshow('Original',image)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Grayscale', grayscale)
    f
# Test
"""
X = np.array(pd.read_csv('./Data/Test/X.csv', header=None))
uNgang = np.array(pd.read_csv('./Data/Test/UNgang.csv', header=None)).T

C = 3
m = 2
"""
dataFolder = "./Data/Image/1024 x 768/"
saveFolder = "./Result/"
nameImage = "1"
#"""
img = Image.open(f"{dataFolder}/{nameImage}.jpg")
X = np.array(img.getdata())
C = 2
uNgang = initUNgang(img, f"{dataFolder}/{nameImage}.txt", f"{dataFolder}/classes.txt", C)
m = 2
#"""

HandleData(f"{dataFolder}/{nameImage}.jpg")
SSSFC(X, uNgang, m, C)


# eSFCM

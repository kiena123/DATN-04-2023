import numpy as np
import pandas as pd
from DoDoThuatToan import *
import cv2
from PIL import Image
from SSSFC import SSSFC

# SSSFC
def randomNewRGB(listColor):
    while(True):
        newRGB = list(np.random.randint(1, 255, size = 3))
        if newRGB not in listColor:
            return newRGB
    
def initUNgang(img, sURLData, sURLCluster, C):
    sizeImg = img.size
    __Clusters = list("0")
    __UNgang = pd.DataFrame(np.zeros( shape = (sizeImg[0]*sizeImg[1], C), dtype = int))
    __ColorCluster = list([(0, 0, 0)])
    __Img_White = np.array(Image.new(img.mode, img.size, (255, 255, 255)))

    for vung in np.loadtxt(sURLData):
        if str(vung[0]) not in __Clusters:
            __Clusters.append(str(vung[0]))
            __ColorCluster.append(randomNewRGB(__ColorCluster))
            
        for height in range(int(vung[2]*sizeImg[1]), int((vung[2]+vung[4])*sizeImg[1])):
            for width in range(int(vung[1]*sizeImg[0]), int((vung[1]+vung[3])*sizeImg[0])):
                __UNgang.loc[height*sizeImg[0]+width, __Clusters.index(str(vung[0]))] = 1
                __Img_White[height, width] = __ColorCluster[__Clusters.index(str(vung[0]))]
        
    print("Da luu anh background trang")
    Image.fromarray(__Img_White).save(f"{saveFolder}/ImgBackgroundWhite.png", format = "png")
    print("Da luu U ngang")
    __UNgang.to_csv(f"{saveFolder}/UNgang.csv", index = False, header= False, mode="w")
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

dataFolder = "./Data/Image/"
saveFolder = "./Result/"
nameImage = "1"

img = Image.open(f"{dataFolder}/{nameImage}.jpg")
X = np.array(img.getdata())
C = 2
uNgang = initUNgang(img, f"{dataFolder}/{nameImage}.txt", f"{dataFolder}/classes.txt", C)
m = 2

# HandleData(f"{dataFolder}/{nameImage}.jpg")
U, V, J = SSSFC(X, uNgang, m, C, nguong = 0.001)
print("DB")
print(DB(X, V, C, U))
print("IFV")
print("PBM")
print("SSWC")

# eSFCM

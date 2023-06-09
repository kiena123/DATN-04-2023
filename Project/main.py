import numpy as np
import pandas as pd
from DoDoThuatToan import *
import cv2
from PIL import Image

urlImg = "D:/DHTL/Nam 4-2/DoAnTotNghiep/Project/Data/Test/Mau/1.jpg"
urlSaveImg = "D:/DHTL/Nam 4-2/DoAnTotNghiep/Project/Data/Test/Splited/1.png"
# vung = list([1, 0.3, 0.3, 0.3, 0.3])
vung = list([ 1, 0.152832, 0.487630, 0.299805, 0.300781])

imageInput = np.array(Image.open(urlImg))
sizeImg = imageInput.shape
heightImg = list(( int(vung[2]*sizeImg[0]) - int(vung[4]*sizeImg[0]/2), int(vung[2]*sizeImg[0]) + int(vung[4]*sizeImg[0]/2)))
widthImg =  list(( int(vung[1]*sizeImg[1]) - int(vung[3]*sizeImg[1]/2), int(vung[1]*sizeImg[1]) + int(vung[3]*sizeImg[1]/2)))

newImg = imageInput[ heightImg[0]: heightImg[1], widthImg[0]: widthImg[1]]

Image.fromarray(np.array(newImg)).save(urlSaveImg, format = "png")
print("End")

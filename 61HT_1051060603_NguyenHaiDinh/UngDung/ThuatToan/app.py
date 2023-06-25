from tkinter.ttk import *
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import ImageTk, Image
#
from DoDoThuatToan import *
from SSSFC import SSSFC
from eSFCM import eSFCM
# from SSFCMBP import SSFCMBP
#
import numpy as np
import pandas as pd
import math 


imgImport = ""
inputImgLabel = ""
resultImgLabel = ""
app = Tk()
appLoading = ""
X = ""
C = 0
m = 0
N = 0
r = 0
eps = 0.1
U1 = ""
U = ""
V = ""
    
# Event

def HandleBtnChonAnh():
    urlImg = filedialog.askopenfilename(filetypes = (("Text images","*.png"), ("Text images","*.jpg"),("all files","*.*")))
    if urlImg == "":
        return
    imgImport = urlImg
    img_import = Image.open(urlImg)
    img_import.save("./Result/inputImage.png")
    img_resized = img_import.resize((700, 300), Image.ANTIALIAS)
    img_display = ImageTk.PhotoImage(img_resized)
    inputImgLabel.configure(image = img_display)
    inputImgLabel.image = img_display
    inputImgLabel.configure(width = 700)
    inputImgLabel.configure(height = 300)
    
def HandleBtnChonFileTxT():
    urlTxt = filedialog.askopenfilename(filetypes = (("Text files","*.txt"),("all files","*.*")))
    if urlTxt == "":
        return
    img_import = Image.open("./Result/inputImage.png")
    img_import = np.array(img_import)
    sizeImg = img_import.shape
    __UNgang = np.ones( shape = (sizeImg[0], sizeImg[1]), dtype = int)*-1
    dataTxt = np.loadtxt(urlTxt)
    if len(dataTxt.shape) == 1:
        dataTxt = np.array([dataTxt])
    
    for vung in dataTxt:
        label = int(float(str(vung[0])))
        heightImg = list(( int(vung[2]*sizeImg[0]) - int(vung[4]*sizeImg[0]/2), int(vung[2]*sizeImg[0]) + int(vung[4]*sizeImg[0]/2)))
        widthImg =  list(( int(vung[1]*sizeImg[1]) - int(vung[3]*sizeImg[1]/2), int(vung[1]*sizeImg[1]) + int(vung[3]*sizeImg[1]/2)))
        # print("height : ", heightImg[0], " to ", heightImg[1])
        # print("width : ", widthImg[0], " to ", widthImg[1])
        __UNgang[ heightImg[0]: heightImg[1], widthImg[0]: widthImg[1]] = label
        img_import[ heightImg[0]: heightImg[1], widthImg[0]: widthImg[1]] = (0, 0, 0) if label == 0 else (round(255/label),round(255/label),round(255/label))

    print(img_import[0, 0])
    pd.DataFrame(__UNgang).to_csv(f"./Result/LabelImg.csv", index = False, header= True, mode="w")
    Image.fromarray(img_import).save(f"./Result/inputImageTxt.png")

    img_import = Image.open("./Result/inputImageTxt.png")
    img_resized = img_import.resize((700, 300), Image.ANTIALIAS)
    img_display = ImageTk.PhotoImage(img_resized)
    inputImgLabel.configure(image = img_display)
    inputImgLabel.image = img_display

def HandleSegment():
    global X, C, m, eps, maxStep, N, r, U1, U, V
    
    imageInput = np.array(Image.open("./Result/inputImage.png"))
    C = int(float(txt_1_2_1.get("1.0",END)))
    m = int(float(txt_1_2_2.get("1.0",END)))
    lamda = float(txt_1_2_3.get("1.0",END))
    eps = float(txt_1_2_4.get("1.0",END))
    maxStep = int(float(txt_1_2_5.get("1.0",END)))
    print( C, " ", m, " ", lamda, " ", eps, " ", maxStep)
    if C < 2:
        messagebox.show("Message", "K > 1")
        return
    if maxStep < 2:
        messagebox.show("Message", "maxStep > 1")
        return
    X = imageInput.reshape((imageInput.shape[0]*imageInput.shape[1], imageInput.shape[-1]))
    N, r = X.shape
    U1 = np.zeros(shape = (imageInput.shape[0]*imageInput.shape[1], C))
    U1csv = np.array(pd.read_csv("./Result/LabelImg.csv", header = None), dtype = int)[1:, :]
    U1csv = U1csv.reshape((U1csv.shape[0]*U1csv.shape[1]))

    for i in range(N):
        if U1csv[i] >= 0:
            U1[i, U1csv[i]] = 1

    sThuatToan = cb_1_3_1.get().strip()
    if sThuatToan == "SSSFC":
        U, V = SSSFC(X, U1, C, m, eps, maxStep)
    elif sThuatToan == "eSFCM":
        U, V = eSFCM(X, U1, C, m, eps, maxStep, lamda)
    elif sThuatToan == "SSFCMBP":
        U, V = SSFCMBP(X, U1, C, m, eps, maxStep)
    else :
        messagebox.show("Message", "Not found")
        return

    # print(U)
    print(V)
    
    pd.DataFrame(U1).to_csv(f"./Result/U1.csv", index = False, header= False, mode="w")
    pd.DataFrame(U).to_csv(f"./Result/U.csv", index = False, header= False, mode="w")

    shapeNewX = imageInput.shape
    newX = np.array(imageInput) 

    for height in range(shapeNewX[0]):
        for width in range(shapeNewX[1]):
            k = height*shapeNewX[1] + width
            index = int(np.argmax(U[k]))
            for i in range(shapeNewX[-1]):
                newX[height, width, i] = int(np.matmul(U[k], V[:, i]))

    '''
    print("-------------")
    print(newX)
    print("-------------")

    '''
    
    Image.fromarray(newX).save("./Result/resultImage.png")
    img_import = Image.open("./Result/resultImage.png")
    img_resized = img_import.resize((700, 300), Image.ANTIALIAS)
    img_display = ImageTk.PhotoImage(img_resized)
    resultImgLabel.configure(image = img_display)
    resultImgLabel.image = img_display
    resultImgLabel.configure(width = 700)
    resultImgLabel.configure(height = 300)
    
    return 

def HandleClusteringResults():
    appResult = Tk()
    appResult.title("Result")
    appResult.geometry("500x200")
    appResult.attributes("-topmost", True)
    
    sResult = cb_1_4_1.get().strip()
    if sResult == "Centers":
        for j in range(C):
            nameCell = Label(appResult, text = "Center " + str(j), font=('Arial',16,'bold'))
            nameCell.grid(row= j, column = 0, padx=10, pady=10)
            for i in range(r):
                cell = Label(appResult, text = str(V[j, i]), font=('Arial',16,'bold'))
                cell.grid(row=j , column=i + 1, padx=10, pady=10)
    else :
        messagebox.show("Message", "Not Support ")
        appResult.mainloop()
        return

    appResult.mainloop()

def HandleClusteringValidity():
    appResult = Tk()
    appResult.title("Result")
    appResult.geometry("500x200")
    appResult.attributes("-topmost", True)
    
    sResult = cb_1_5_1.get().strip()
    if sResult == "DB":
        cell = Label(appResult, text = "Do do thuat toan DB : " + str(round(DB(X, V, C, U), 6)), bg = "white", font=('Arial',16,'bold'))
        cell.grid(row=0, column= 0, padx=10, pady=10)
    elif sResult == "IFV":
        cell = Label(appResult, text = "Do do thuat toan IFV : " + str(round(IFV(X, V, C, U), 6)), bg = "white", font=('Arial',16,'bold'))
        cell.grid(row=0, column= 0, padx=10, pady=10)
    elif sResult == "PDM":
        cell = Label(appResult, text = "Do do thuat toan PDM : " + str(round(PDM(X, V, C, U), 6)), bg = "white", font=('Arial',16,'bold'))
        cell.grid(row=0, column= 0, padx=10, pady=10)
    else :
        messagebox.showinfo("Message", "Not Support ")
        appResult.mainloop()
        return

    appResult.mainloop()


app.title("Dinh's app")
# window.geometry("1024x700")
# app.maxsize(1024,700)
app.minsize(1024,700)
# app.config(bg="skyblue")
    
frame_1 = Frame(app, width= 300, height= 680)
frame_1.grid(row=0, column= 0, padx=10, pady=10)

#   Input file data
frame_1_1 = Frame(frame_1, width= 500, height= 500, bg='white')
frame_1_1.grid(row=0, column= 0, padx=5, pady=10)

Label(frame_1_1, text="Input file data", bg = "red", fg = "white").grid(row=0, column=0, padx = 10 , pady=5)
Button(frame_1_1, text = "Chon anh ve tinh", command = HandleBtnChonAnh).grid(row=1, column= 0, padx=5, pady=10)
Button(frame_1_1, text = "Chon file txt bo tro", command = HandleBtnChonFileTxT).grid(row=2, column= 0, padx=5, pady=10)

#   Input arguments
frame_1_2 = Frame(frame_1, width= 300, height= 300, bg='white')
frame_1_2.grid(row=1, column= 0, padx=5, pady=10)

Label(frame_1_2, text="Input arguments", bg = "red", fg = "white").grid(row=0, column=0, padx= 10 , pady=5)
frame_1_2_1 = Frame(frame_1_2, width= 300, height= 300, bg='white')

    # Number of Clusters ( So cum )
Label(frame_1_2_1, text="Number of Clusters (K): ").grid(row=0, column=0)
txt_1_2_1 = Text(frame_1_2_1, height = 1, width = 10)
txt_1_2_1.insert(END, "2")
txt_1_2_1.grid(row=0, column=1, padx= 10 , pady=5)
frame_1_2_1.grid(row=1, column= 0, padx=5, pady=10)

    # Weighting expoment ( trọng số )
Label(frame_1_2_1, text="Weighting expoment (m): ").grid( row=1, column=0)
txt_1_2_2 = Text(frame_1_2_1, height = 1, width = 10)
txt_1_2_2.insert(END, "2")
txt_1_2_2.grid(row=1, column=1, padx= 10 , pady=5)

    # Lamda number (lamda)
Label(frame_1_2_1, text="Lamda number (lamda): ").grid( row=2, column=0)
txt_1_2_3 = Text(frame_1_2_1, height = 1, width = 10)
txt_1_2_3.insert(END, "1")
txt_1_2_3.grid(row=2, column=1, padx= 10 , pady=5)

    # Min amount of improvement ( Mức độ cải thiện tối thiểu )
Label(frame_1_2_1, text="Min amount of improvement (eps): ").grid( row=3, column=0, padx= 10 , pady=5)
txt_1_2_4 = Text(frame_1_2_1, height = 1, width = 10)    
txt_1_2_4.insert(END, "0.01")
txt_1_2_4.grid(row=3, column=1, padx= 10 , pady=5)
    
    # Max number of iterations ( Số lần lặp tối đa )
Label(frame_1_2_1, text="Max number of iterations (maxStep)").grid( row=4, column=0, padx= 10 , pady=5)
txt_1_2_5 = Text(frame_1_2_1, height = 1, width = 10)    
txt_1_2_5.insert(END, "150")
txt_1_2_5.grid(row=4, column=1, padx= 10 , pady=5)

#   Choose algorithms
frame_1_3 = Frame(frame_1, width= 500, height= 500, bg='white')
frame_1_3.grid(row=3, column= 0, padx=5, pady=10)
Label(frame_1_3, text="Choose algorithms", bg = "red", fg = "white").grid(row=0, column=0, padx = 10 , pady=5)
cb_1_3_1 = Combobox(frame_1_3)
# cb_1_3_1['values']= ("SSSFC", "eSFCM", "SSFCMBP")
cb_1_3_1['values']= ("SSSFC", "eSFCM")
cb_1_3_1.current(0)
cb_1_3_1.grid(row=1, column= 0, padx=5, pady=10)
Button(frame_1_3, text = "Segment", command = HandleSegment).grid( row=1, column=1, padx = 10 , pady=5)
    
#   Clustering Results
frame_1_4 = Frame(frame_1, width= 500, height= 500, bg='white')
frame_1_4.grid(row=4, column= 0, padx=5, pady=10)
Label(frame_1_4, text="Clustering Results", bg = "red", fg = "white").grid(row=0, column=0, padx = 10 , pady=5)
frame_1_4_1 = Frame(frame_1_4, width= 500, height= 500, bg='white')
frame_1_4_1.grid(row=1, column= 0, padx=5, pady=10)
cb_1_4_1 = Combobox(frame_1_4_1)
# cb_1_4_1['values']= ("Centers", "Membership matrix")
cb_1_4_1['values']= ("Centers")
cb_1_4_1.current(0)
cb_1_4_1.grid(row=0, column= 0, padx=5, pady=10)
Button(frame_1_4_1, text = "OK", command = HandleClusteringResults).grid(row=0, column=1, padx = 10 , pady=5)

#   Clustering Validity
frame_1_5 = Frame(frame_1, width= 500, height= 500, bg='white')
frame_1_5.grid(row=5, column= 0, padx=5, pady=10)
Label(frame_1_5, text="Clustering Validity", bg = "red", fg = "white").grid(row=0, column=0, padx = 10 , pady=5)
frame_1_5_1 = Frame(frame_1_5, width= 500, height= 500, bg='white')
frame_1_5_1.grid(row=1, column= 0, padx=5, pady=10)
cb_1_5_1 = Combobox(frame_1_5_1)
# cb_1_5_1['values']= ("DB", "IFV", "PDM", "SSWC")
cb_1_5_1['values']= ("DB", "IFV", "PDM")
cb_1_5_1.current(0)
cb_1_5_1.grid(row=0, column= 0, padx=5, pady=10)
Button(frame_1_5_1, text = "OK", command = HandleClusteringValidity).grid(row=0, column=1, padx = 10 , pady=5)


frame_2 = Frame(app, bg='grey')
frame_2.grid(row=0, column=1, padx=10, pady=10)
    
#   Input image
frame_2_1 = Frame(frame_2, width= 630, height= 400, bg='white')
frame_2_1.grid(row=0, column= 0, padx=5, pady=10)
Label(frame_2_1, text="Original image").grid(row=0,column=0, padx=5, pady=5)
inputImgLabel = Label(frame_2_1, width= 100, height= 20)
inputImgLabel.grid(row=1 ,column= 0, padx=5, pady=5)

#   Result image
frame_2_2 = Frame(frame_2, bg='white')
frame_2_2.grid(row=1, column= 0, padx=5, pady=10)
Label(frame_2_2, text="Segmented image").grid(row=0,column=0, padx=5, pady=5)
resultImgLabel = Label(frame_2_2, width= 100, height= 20)
resultImgLabel.grid(row=1 ,column= 0, padx=5, pady=5)

app.mainloop()


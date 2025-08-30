import math
import os

import numpy as np
import matplotlib.pyplot as plt
import cv2

#hàm cân bằng ảnh dùng hàm log
def convert_Logarithm(imgs, c):
    newList = []
    for i in imgs:
        i = i.astype(float)
        newList.append(float(c)* cv2.log(1+i))
    return newList

#hàm cân bằng ảnh dùng hàm mũ
def convertByPowerLaw(imgs, gamma, c):
    img_new =[]
    for i in imgs:
        k = i.astype(float)
        img_new.append(float(c) * pow(k, float(gamma)))
    return img_new

#hàm chuyển danh sách ảnh sang ảnh xám
def convertGray(imgs):
    imgGray = []
    for i in imgs:
        gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        imgGray.append(gray)
    return imgGray

#Hàm lấy danh sách ảnh từ file và lưu vào mảng
def getListImage(imgName):
    files = os.listdir(imgName)
    listnameImg =[f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    listImg = []
    for f in listnameImg:
        path = os.path.join('IMG', f)
        img = cv2.imread(path)
        listImg.append(img)
    return listImg

#Hàm in danh sách ảnh
def showListImage(listimg):
    size = len(listimg)
    cols = 4
    rows = math.ceil(size/cols)
    plt.figure(figsize=(20, rows*5))
    for idx, img in enumerate(listimg):
        plt.subplot(rows, cols, idx+1)
        plt.imshow(img[:,:,::-1])
        plt.axis('off')
    plt.show()

#Hàm in danh sách ảnh xám
def showListImageGray(listimg):
    size = len(listimg)
    cols = 4
    rows = math.ceil(size/cols)
    plt.figure(figsize=(20, rows*5))
    for idx, img in enumerate(listimg):
        plt.subplot(rows, cols, idx+1)
        plt.imshow(img, cmap = 'gray')
        plt.axis('off')
    plt.show()

# Thuật toán cân bằng ảnh bằng histogram
def histogram(img):
    copy = img.copy()
    hist,_ = np.histogram(copy, bins = 256, range = (0, 256))
    pdf = hist/hist.sum()
    cdf =  np.cumsum(pdf)
    mapping = np.round(cdf * 255).astype(np.uint8)
    copy = copy.astype(np.uint8)
    equalized = mapping[copy]
    return equalized

list = getListImage("IMG")
imgGrays = convertGray(list)

imgLo = convert_Logarithm(imgGrays, 2)

imgHis = histogram(imgLo[1])
imhHis1 = cv2.equalizeHist(imgLo[1].astype(np.uint8))
plt.figure(figsize=(20, 5))
plt.imshow(imgHis, cmap = 'gray')
plt.subplot(1, 2, 1)
plt.imshow(imhHis1, cmap = 'gray')
plt.subplot(1, 2, 2)
plt.axis('off')
plt.show()


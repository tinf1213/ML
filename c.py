import joblib
import requests
import numpy as np
from matplotlib import pyplot as plt
import datetime
import time
import cv2
import os
import PIL
from sklearn.preprocessing import StandardScaler
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
import time


clf = joblib.load('kaptcha.pkl')
def saveKaptcha(image, dest):   #抓取網頁目標驗證碼圖片並加工
    scaler = StandardScaler()
    pil_image = PIL.Image.open(image).convert('RGB')
    open_cv_image = np.array(pil_image)
    nc = cv2.fastNlMeansDenoisingColored(open_cv_image, None, 13, 13, 7, 21)
    imgray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(imgray, 180, 255, 0, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x: x[1])
    ary=[]
    for (c, _) in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if x < 70 and w > 6 and w < 20 and h >= 10 and x > 0:
            ary.append((x, y, w, h))
    data=[]
    for idx, (x,y,w,h) in enumerate(ary):
        fig = plt.figure()
        roi = open_cv_image[y:y+h, x:x+w]
        thresh = roi.copy()
        os.chdir('C:/Users/ericd/PycharmProjects/pythonProject1/data/practice')
        with open('{}.png'.format(idx), 'wb') as file:
            cv2.imwrite('{}.png'.format(idx), thresh)
def predict(dest):                 #產生預測
        data=[]
        os.chdir('C:/Users/ericd/PycharmProjects/pythonProject1/data/practice')
        for idx, img in enumerate(os.listdir(os.getcwd())):
            pil_image = PIL.Image.open('{}'.format(img)).convert('1')
            img = pil_image.resize((19,15), PIL.Image.Resampling.LANCZOS)
            data.append([pixel for pixel in iter(img.getdata())])
        scaler = StandardScaler()
        scaler.fit(data)
        data_scaled = scaler.transform(data)
        return clf.predict(data_scaled)
for k in range(100):
    counter = 0
    os.chdir('C:/Users/ericd/PycharmProjects/pythonProject1/data/practice')
    for i in os.listdir():
        os.remove(i)
    path = "C:/Users/ericd/PycharmProjects/pythonProject1/chromedriver.exe"
    driver = webdriver.Chrome(path)
    os.chdir("C:/Users/ericd/PycharmProjects/pythonProject1/data")
    driver.get("https://ap.ceec.edu.tw/RegExam/User/PRegLogin/?examtypes=A")
    element = driver.find_element_by_id("valiCode")
    driver.save_screenshot('screenshot.png')
    left = element.location['x']
    top = element.location['y']
    right = element.location['x'] + element.size['width']
    bottom = element.location['y'] + element.size['height']
    im = Image.open('screenshot.png')
    im = im.crop((left, top, right, bottom))
    im.save('screenshot.png')
    saveKaptcha('screenshot.png','imagedata')
    re = predict('imagedata')

    if len(re) > 4:
        if re[2] == 10:
            re = np.delete(re,4)
        else:
            re = np.delete(re,2)
    if len(re) < 3:
        print("Error")
        driver.close()
        counter -= 1
        continue
    if re[1] == 10:
        print("Error")
        driver.close()
        counter -= 1
        continue
    if len(re) == 4:
        ans = re[0] * 10 + re[1] + re[3]
        re = np.delete(re, 2)
    elif re[0] != 10 and re[1] != 10 and re[2] != 10:
        ans = re[0] * 10 + re[1] + re[2]
    else:
        print("error")
        driver.close()
        counter -= 1
        continue

    validatecodebox = driver.find_element_by_name("pRegLogin.Captcha")

    anstr = []
    anstr.append(re[0])
    anstr.append(re[1])
    anstr.append('+')
    anstr.append(re[2])
    for i in anstr:
        print(i, end='')
    print()
    print(ans)
    fillin = ""
    fillin += str(ans)
    validatecodebox.send_keys(fillin)
    time.sleep(1)
    driver.close()
print(counter/100)

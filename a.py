import requests
import numpy
import PIL
import os
import shutil
import cv2
from PIL import Image
from matplotlib import pyplot as plt

index = 0
number = 0
for index in range(1):
    with open('kaptcha.jpg', 'wb') as file:
        res = requests.get('https://ap.ceec.edu.tw/RegInfo/Account/CaptchaImage', verify = True)
        file.write(res.content)
    image = cv2.imread('kaptcha.jpg')
    open_cv_image = numpy.array(image)
    nc = cv2.fastNlMeansDenoisingColored(open_cv_image, None, 13, 13, 7, 21)
    imgray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(imgray, 180, 255, 0, cv2.THRESH_BINARY)
    #plt.imshow(thresh)
    #plt.show()
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key = lambda x: x[1])
    ary = []
    for (c, _) in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w > 10: print((x, y, w, h))
        if x < 70 and w >= 6 and w < 15 and h >= 10 and x > 0:
            ary.append((x, y, w, h))
            print("This")
            print((x, y, w, h))
    for id, (x, y, w, h) in enumerate(ary):
        roi = imgray[y:y + h, x:x + w]
        thresh = roi.copy()
        with open('{}.jpg'.format(number), 'wb') as f:
            cv2.imwrite('{}.jpg'.format(number), thresh)
        number = number + 1
        print(number)



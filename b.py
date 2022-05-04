import os
from sklearn.preprocessing import StandardScaler
import PIL.Image
import cv2
from PIL import Image
from matplotlib import pyplot
import numpy
from sklearn.neural_network import MLPClassifier
import joblib

digits = []
lables = []
basewide = 50
for index in range(0,11):
    os.chdir('C:/Users/ericd/PycharmProjects/pythonProject1/data/{}'.format(index))
    print(os.getcwd())
    #print(os.listdir())
    for counter in range(0,50):
        image = Image.open('{}.jpg'.format(counter))
        img = image.resize((19,15), PIL.Image.Resampling.LANCZOS)
        digits.append([pixel for pixel in iter(img.getdata())])
        lables.append(index)

digit_ary = numpy.array(digits)
#print(digit_ary.shape)

scalar = StandardScaler()
scalar.fit(digit_ary)
x_scalar = scalar.transform(digit_ary)
mlp = MLPClassifier(activation='logistic',max_iter=10000)
mlp.fit(x_scalar,lables)

predicted = mlp.predict(x_scalar)
target = numpy.array(lables)
print('模型得分:{:.2f}'.format(mlp.score(x_scalar,target)))
os.chdir("C:/Users/ericd/PycharmProjects/pythonProject1")
joblib.dump(mlp, 'kaptcha.pkl')
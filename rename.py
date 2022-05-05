import os
p = os.getcwd()
os.chdir(p + '/data')
p = p + '/data/'
file = os.listdir()
index = 0
print(file)
for k in range(11):
    path = str(k)
    index += 1
    temp = p + path
    os.chdir(temp)
    #print(os.getcwd())
    files = os.listdir(p+path)
    #print(files)
    n = 0
    re = 50
    for i in files:
        old = i
        #os.chdir(path)
        new = str(re)+'.jpg'
        os.rename(old, new)
        re += 1

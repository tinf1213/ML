import os
p = 'C:/Users/ericd/PycharmProjects/pythonProject1/data'
os.chdir(p)
file = os.listdir()
index = 0
print(file)
for k in range(11):
    path = str(k)
    index += 1
    p = p + "/"
    os.chdir(p+path)
    #print(os.getcwd())
    files = os.listdir(p+path)
    #print(files)
    n = 0
    re = 0
    for i in files:
        old = i
        #os.chdir(path)
        new = str(re)+'.jpg'
        os.rename(old, new)
        re += 1
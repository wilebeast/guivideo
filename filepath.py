import os

url = "http://file.iqilu.com/custom/new/v2016/images/logo.png"

(file, ext) = os.path.splitext(url)
print(file)
print(ext)

(path, filename) = os.path.split(url)
print(filename)
print(path)
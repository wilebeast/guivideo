from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from convert import start_convert


def selectPath():
    path_ = askdirectory()
    path.set(path_)


def selectFile():
    file_ = askopenfilename()
    file.set(file_)


def convert():
    if not file.get():
        warning.set("请选择原始文件!")
        return

    warning.set("开始转化")
    print(file.get())
    start_convert(file.get())
    warning.set("文件转化成功")


root = Tk()
root.title("视频转化工具")
path = StringVar()
file = StringVar()
warning = StringVar()

Label(root, text="原文件:").grid(row=0, column=0)
Entry(root, textvariable=file).grid(row=0, column=1)
Button(root, text="文件选择", command=selectFile).grid(row=0, column=2)

# Label(root, text="目标路径:").grid(row=1, column=0)
# Entry(root, textvariable=path).grid(row=1, column=1)
# Button(root, text="路径选择", command=selectPath).grid(row=1, column=2)

Button(root, text="开始执行", command=convert).grid(row=2, column=0)
Entry(root, textvariable=warning).grid(row=2, column=1)

root.mainloop()


import tkinter as tk
import tkinter.messagebox
from tkinter import scrolledtext
import threading
from tkinter import filedialog

from PyPDF2 import PdfFileReader, PdfFileWriter



class PDF():

    def __init__(self, file_paths, scr, filename):
        self.file_paths = file_paths
        file = filename.split('.')
        if file[-1] == 'pdf':
            self.filename = filename
        else:
            self.filename = filename + '.pdf'

        self.scr = scr
        self.lis = []
        self.count = 0
        self.view()
        if self.file_paths:
            self.mer()
        else:
            self.scr.insert('end', "-----未选择文件，请重新开始----")

    def view(self):
        for file_path in self.file_paths:
            self.count += 1
            self.scr.insert('end', "{}.{} \n".format(self.count, file_path))
            self.scr.see('end')

    def mer(self):
        try:
            output = PdfFileWriter()
            outputpage = 0
            for pdfpath in self.file_paths:

                input = PdfFileReader(open(pdfpath, 'rb'), strict=False)
                pagecount = input.getNumPages()
                outputpage += pagecount
                for ipage in range(pagecount):
                    output.addPage(input.getPage(ipage))

            outputstream = open(self.filename, 'wb')
            output.write(outputstream)
            self.scr.insert('end', "\n\n")
            self.scr.insert('end', "-----{}文件  合并完成----".format(self.filename))

        except:
            self.scr.insert('end', "\n\n")
            self.scr.insert('end', "-----合并失败，请求帮助----")

        self.scr.see('end')


def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()

def thread_spi(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()


def start():

    flag = False
    fm = file_name.get()
    if fm == '':
        tk.messagebox.showerror('填写不得为空')
    else:
        flag = True

    file_paths = []
    filenames = tk.filedialog.askopenfiles()
    for filename in filenames:
        path = filename.name
        file_paths.append(path)


    if flag:
        startview = tk.Toplevel(window)
        startview.resizable(width=False, height=False)
        startview.geometry('500x300')
        # 滚动条
        scr = scrolledtext.ScrolledText(startview, width=55, height=15)  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
        scr.place(x=50, y=50)
        PDF(file_paths, scr, fm)

if __name__ == '__main__':
    window = tk.Tk()
    window.title('傻逼逼合并pdf专属软件')
    window.resizable(width=False, height=False)
    window.geometry('400x500')
    window.update()

    tk.Label(window, text='PDF多个合并', bg='red', font=('Arial', 12), width=25, height=2).pack()

    tk.Label(window, text="合并后文件名：").place(x=80, y=160)
    file_name = tk.StringVar()
    file_name.set('合并.pdf')
    entry_file_name = tk.Entry(window,textvariable=file_name).place(x=180, y=160)

    button_start = tk.Button(window, text='Start', command=lambda: thread_it(start))
    button_start.place(x=200, y=350)
    tk.Label(window, text="版本： v1.0", font=('Arial', 8)).place(x=260, y=440)
    window.mainloop()






import tkinter
root = tkinter.Tk()
root.title("雅虎雅虎")
root.geometry("500x300")

class srk:
    def __init__(self,a,b):
        self.a = a
        self.b = b
        for i in range(a):
            input_user = tkinter.Entry(root)
            input_user.pack(2,8)
root.mainloop()
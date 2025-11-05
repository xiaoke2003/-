import tkinter as tk


def show_frame(frame):
    # 隐藏所有 frame
    for f in frames.values():
        f.pack_forget()
    # 显示目标 frame
    frame.pack(fill='both', expand=True)


root = tk.Tk()
root.title("窗口内页面切换")

# 创建两个 frame，分别代表两个页面
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)

frames = {
    "frame1": frame1,
    "frame2": frame2
}

# 在 frame1 中添加内容
label1 = tk.Label(frame1, text="这是页面 1")
label1.pack(pady=10, padx=10)
button1 = tk.Button(frame1, text="跳转到页面 2", command=lambda: show_frame(frame2))
button1.pack(pady=10, padx=10)

# 在 frame2 中添加内容
label2 = tk.Label(frame2, text="这是页面 2")
label2.pack(pady=10, padx=10)
button2 = tk.Button(frame2, text="跳转到页面 1", command=lambda: show_frame(frame1))
button2.pack(pady=10, padx=10)

# 初始显示 frame1
show_frame(frame1)

root.mainloop()
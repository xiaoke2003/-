import tkinter as tk

root = tk.Tk()
root.title("Checkbutton 模拟方形单选")
root.geometry("300x200")

# 1. 为每个选项创建独立变量（Checkbutton 默认需要独立变量）
var1 = tk.BooleanVar(value=True)  # 选项1默认勾选
var2 = tk.BooleanVar(value=False)
var3 = tk.BooleanVar(value=False)

# 2. 互斥控制函数：点击一个选项时，取消其他选项
def select_only(var_selected, var_list):
    if var_selected.get():  # 如果当前选项被勾选
        for var in var_list:
            if var != var_selected:
                var.set(False)  # 取消其他选项

# 3. 创建方形 Checkbutton（自带方形样式），绑定互斥函数
check1 = tk.Checkbutton(
    root,
    text="选项1（默认勾选）",
    variable=var1,
    command=lambda: select_only(var1, [var1, var2, var3]),
    font=("黑体", 12)
)
check1.pack(pady=(30, 10))

check2 = tk.Checkbutton(
    root,
    text="选项2",
    variable=var2,
    command=lambda: select_only(var2, [var1, var2, var3]),
    font=("黑体", 12)
)
check2.pack(pady=10)

check3 = tk.Checkbutton(
    root,
    text="选项3",
    variable=var3,
    command=lambda: select_only(var3, [var1, var2, var3]),
    font=("黑体", 12)
)
check3.pack(pady=10)

root.mainloop()
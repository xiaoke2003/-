import random,time
import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText  # 引入正文模块
from email.header import Header  # utf-
from pymysql import connect

#开始连接账号数据库
con = connect(user="root", password="root", port=3306)
cr = con.cursor()
sql_index = 0
cr.execute("show databases;")
data_tuple = cr.fetchall()
print(data_tuple)
data_list = ["create database zhanghao default character set utf8;",  # 执行ddl语句创建数据库
            "create table youxiang(yx varchar(20),mm varchar(20));",  # 创建表
            "alter table youxiang add column yx varchar(20), add column mm varchar(20);"  # 为空表添加列
            ]
def show_data(data_tuple):
    tf = False
    for sun_tuple in data_tuple:
        if "zhanghao" in sun_tuple:
            print(f"zhanghao存在于{sun_tuple}")
            tf = True
            break

    if not tf:
        print(f"zhanghao不存在\ntry_create")
        try:
            cr.execute(f"create database zhanghao default character set utf8;")
            print(f"zhanghao已创建")
            cr.execute(f"use zhanghao")
            cr.execute("create table yx_and_mm(my_id int,yx varchar(20),mm varchar(20),jzmm varchar(20));")
            cr.execute("create table dl_date(zh varchar(20),date timestamp,mm varchar(20));")# 这里暂时先故意写死表和列，后续再开放
            cr.execute("alter table yx_and_mm add primary key(my_id);")
            cr.execute("alter table yx_and_mm modify my_id int auto_increment;")
            print("数据结构搭建完成,可以插入数据")
        except:
            print(f"zhanghao创建失败了")
show_data(data_tuple)

#------------------------------------------------------------------------------------------------------------------
# 访问数据库中的记住密码
# 对未来的自己宣布，因自己记忆力不好而在10月28日调整代码所产生的bug不明原因，直接原因是因为我通过mysql客服端手动清除了数据库，
# 重新创建之后索引就出问题了，本来最先想到的是通过try跳过索引代码，后来突发奇想想要定一个函数实现清除数据库重新出创建，不知道为什么。
# 好像是因为数据库中的表是完全空状态，导致的无法索引indexerror，但是解决途中脑子绕柱了，不知道怎么解了，就困扰了我几天。
# 最后决定暂时先用当时第一时间想到的try办法。只能这样了，不然运行都运行不起来。
cr.execute("use zhanghao;")
cr.execute("select jzmm from yx_and_mm;")
return_jzmm = cr.fetchall()
try:
    get_jzmm = return_jzmm[0][0]
except IndexError:
    get_jzmm = ""
    print("记住密码列不存在")
#结束
#-------------------------------------------------------------------------------------------------------------------
#开始加载ui
root = tk.Tk()

# 计算中轴线
win_width_height = {"width":500,"height":500}

getscreen_width = root.winfo_screenwidth()
getscreen_height = root.winfo_screenheight()
screen_width = getscreen_width // 2
screen_height = getscreen_height // 2
win_width = win_width_height["width"] // 2
win_height = win_width_height["height"] //2
x = screen_width - win_width  # 窗口宽度的开始值
y = screen_height -win_height  # 窗口高度的开始值
# 设置窗口大小
root.geometry(f"500x500+{x}+{y}")
root.title("哈喽")
root.grid_columnconfigure(1,weight=1)

frem1 = tk.Frame(root)
frem2 = tk.Frame(root)
frem3 = tk.Frame(root)  # 登录以后的界面
wenzi = tk.Label(frem1,text="登录系统")
wenzi.pack(padx=1,pady=1)
# 容器字典
frems = {
#页面1的容器
"frem1" :frem1,  # 登录界面
#页面2的容器
"frem2" : frem2,   # 注册界面
"frem3" : frem3  # 进入界面
}


def show_frem(my_frem):
    # 此函数用来隐藏字典中的所有的容器，之后将指定的参数容器放置
    for i in frems.values():
        i.pack_forget()  # 隐藏完成
    my_frem.pack(fill="both",expand=True)


#--------------------------------------------------------------------------------------------------------------
#获取单选框的默认状态
cr.execute("use zhanghao;")
cr.execute("select jzmm from yx_and_mm;")
try:
    return_bool = cr.fetchall()[1][0]  # 获取第二行的第一个
except IndexError:
    print("判断勾选框的整数值不存在")
    return_bool = 0
#这一行是我的错误代码，下面是豆包的# check_button = tk.BooleanVar(return_bool)
check_button = tk.BooleanVar(master=root, value=bool(int(return_bool)) if return_bool else False)


# 账号
row1_frame = tk.Frame(frem1)  # 实例化一个容器
row1_frame.pack(pady=10)  # 放置容器位置

row1 = tk.Entry(row1_frame)  # 实例化一个输入框,基于row1_frame容器中
get_zh = row1.get()
zh_index = {"已登录账号位置":0,"密码值":0}


#-----------------------------------------------------------------------------------------------------------
#记住账号
# 访问一下zhanghao数据库中的dl——date表，查看dl列中有没有数据，如果有，就把dl列中的最后一个数据读取到，为row1设置默认值。
# 如果没有，那直接就是空值
cr.execute("use zhanghao;")
entry_table_exit = True
cr.execute("show tables;")
entry_table = cr.fetchall()
for i in entry_table:
    if "dl_date" in i:
        print("访问dl_date表时存在")
        cr.execute("select zh from dl_date;")
        column_value = cr.fetchall()
        try:
            get_column_end_value = column_value[-1][0]
        except IndexError:
            print("自动记住登录账号索引错误")
            get_column_end_value = ""
        row1.insert(0,f"{get_column_end_value}")
        entry_table_exit = False
        break
#结束
#---------------------------------------------------------------------------------------------------------------
row1_zh = tk.Label(row1_frame,text="账号：")  # 实例化一个文字依然基于容器

row1_zh.pack(side=tk.LEFT)
row1.pack(side=tk.LEFT)


# 密码
row2_frame = tk.Frame(frem1)
row2_frame.pack(pady=10)
row2_Check_frem = tk.Frame(frem1)
row2_Check_frem.pack()
row2_Check = tk.Checkbutton(row2_Check_frem,
    text="记住密码",
    variable=check_button,
    font=("黑体",10),
    width=9,
)  # 创建记住账号密码勾选框
row2 = tk.Entry(row2_frame)
row2.insert(0,str(get_jzmm))  # 实时获取记住密码的值
row2_mm = tk.Label(row2_frame,text="密码：")
row2_mm.pack(side=tk.LEFT)
row2.pack(side=tk.LEFT)
row2_Check.pack(side=tk.LEFT)
#-----------------------------------------------------------------------------------------------------------------------
# 判断记住密码组件有没有被点击从而决定要不要获取数据库中mm列的值到row2中去




# 计算中轴线——密码正确之后
new_getscreen_width = root.winfo_screenwidth()
new_getscreen_height = root.winfo_screenheight()

new_screen_width = new_getscreen_width // 2
new_screen_height = new_getscreen_height //2

new_win_width = 1280 // 2
new_win_height = 720 //2

new_x = new_screen_width - new_win_width
new_y = new_screen_height - new_win_height


def get_input():

    print("测试专看，用户的账号是{}，用户的密码是{}".format(row1.get(),row2.get()))
    # 启动查询
    cr.execute("use zhanghao;")
    cr.execute("select yx from yx_and_mm;")
    yx_column = cr.fetchall()
    print(f"请管理员查看邮箱列的内容：{yx_column}")
    cr.execute("select mm from yx_and_mm;")
    mm_column = cr.fetchall()
    print(f"请管理员查看邮箱列的内容：{mm_column}")
    yx_list = []
    mm_list = []
    for vaule in yx_column:
        for sun_value in vaule:
            yx_list.append(sun_value)
    for vaule in mm_column:
        for sun_value in vaule:
            mm_list.append(sun_value)
    if row1.get() in yx_list:
        if row2.get() in mm_list:
            print("密码正确")
            messagebox.showinfo("正确","密码正确")
            win_width_height["width"] = 1280
            win_width_height["height"] = 720
            root.geometry(f"{win_width_height["width"]}x{win_width_height["height"]}+{new_x}+{new_y}")
            show_frem(frem3)
            get_time_int = time.time()
            localt_time = time.localtime(get_time_int)
            get_date_time = time.strftime("%Y-%m-%d %H:%M:%S",localt_time)
            get_zh = row1.get()
            get_mm = row2.get()
            print(f"现在时间{get_date_time}")

            insert_dl_tata = "insert into dl_date(zh,date)values(%s,%s)"
            cr.execute(insert_dl_tata, (get_zh, get_date_time))
            print("登录数据已录入")
            con.commit()  # 提交事务

            if check_button.get():
                print("已勾选")
                # 开始找到已经登录账号在数据库列中的索引位置
                cr.execute("use zhanghao;")
                cr.execute("select yx from yx_and_mm")
                mm_tuple = cr.fetchall()
                for index, value in enumerate(mm_tuple):
                    if get_zh in value:
                        zh_index["已登录账号位置"] = index
                        break
                # 获取mm列中的和和账号列有相同索引值的元素。
                cr.execute("use zhanghao;")
                cr.execute("select mm from yx_and_mm")
                mm_tuple = cr.fetchall()
                zh_index["密码值"] = mm_tuple[zh_index["已登录账号位置"]][0]
                # 获取完毕将此值传递给,先存储到中间值中去
                up_data = "update yx_and_mm set jzmm=%s where my_id=1;"
                cr.execute(up_data,(zh_index["密码值"],))
                cr.execute("update yx_and_mm set jzmm=1 where my_id=2;")
                con.commit()


            else:
                print("已取消记住密码")
                #开始更新jzmm列的值为空字符串
                cr.execute("use zhanghao;")
                cr.execute("update yx_and_mm set jzmm='' where my_id=1;")
                cr.execute("update yx_and_mm set jzmm=0 where my_id=2;")
                con.commit()

        else:
            print("密码错误")
            messagebox.showinfo("错误","密码错误")
    else:
        print(f"{row1.get()}账号不存在")
        messagebox.showinfo("错误", "账号不存在，请先进行注册")



    if row1.get() == "" or row2.get() == "":
        print("账号或者密码不能为空，请重新输入")
        messagebox.showinfo("错误","账号或者密码不能为空，请重新输入")

# 编辑登录按钮
button_frame = tk.Frame(frem1)  # 按钮的容器
button = tk.Button(button_frame,
                   text="登录",
                   width=7,
                   command=get_input)

button2 = tk.Button(button_frame,
                   text="注册",
                   width=7,
                    command=lambda : show_frem(frem2)
                   )

button_frame.pack(padx=1,pady=1)
button.pack(side=tk.LEFT,padx=(25,10),pady=(10,130))  # 放置登录按钮
button2.pack(side=tk.LEFT,padx=(40,20),pady=(10,130))  # 放置注册按钮

# 注册系统
# frem2容器包裹的是第二个页面，也就是注册页面
zc_styem = tk.Label(frem2,text="注册系统")
zc_styem.pack(padx=1,pady=1)

frem_sjh = tk.Frame(frem2)
sjh_lb = tk.Label(frem_sjh,text="  邮箱号：")
sjh_lb.pack(side=tk.LEFT,padx=(1,9),pady=(1,9))
sjh_entry = tk.Entry(frem_sjh)
sjh_entry.pack(side=tk.RIGHT,padx=(1,9),pady=(1,9))

frem_mm = tk.Frame(frem2)
mm_lb = tk.Label(frem_mm,text="     密码：")
mm_lb.pack(side=tk.LEFT,padx=(1,9),pady=(1,9))
mm_entry = tk.Entry(frem_mm)
mm_entry.pack(padx=(1,9),pady=(1,9))

frem_mm2 = tk.Frame(frem2)
mm_lb2 = tk.Label(frem_mm2,text="确认密码：")
mm_lb2.pack(side=tk.LEFT,padx=(1,9),pady=(1,9))
mm_entry2 = tk.Entry(frem_mm2)
mm_entry2.pack(padx=(1,9),pady=(1,9))

sjs_jy = None
def yzm():
    account = sjh_entry.get()
    if account == "":
        print("获取到空字符串，可能无法执行发送")
    print("即将sendiong，请稍后")
    sjs = ""
    for i in range(6):
        sjs += str(random.randint(0,9))
    print("please user check：{}".format(sjs))
    # 开始发送

    smt = smtplib.SMTP_SSL("smtp.qq.com", 465)
    smt.ehlo()
    smt.login("2844388638@qq.com", "mfyqvgxtszjtdgdi")
    min = MIMEText("测试", "utf-8")
    min["From"] = "sending<2844388638@qq.com>"
    min["To"] = f"receive<{account}>"
    min["subject"] = Header(f"{sjs}", "utf-8")
    smt.sendmail("2844388638@qq.com", f"{account}",f"{min}")
    smt.quit()
    print("验证码already sending completed")
    global sjs_jy
    sjs_jy = sjs

frem_yzm = tk.Frame(frem2)
lzm_lb = tk.Label(frem_yzm,text="输入随机码：")
lzm_lb.pack(side=tk.LEFT,padx=(1,9),pady=(1,9))
yzm_entry = tk.Entry(frem_yzm,width=10)
yzm_entry.pack(side=tk.LEFT,padx=(1,9),pady=(1,9))
yzm_button = tk.Button(frem_yzm,
                       width=5,
                       text="发送",
                       command = lambda : yzm())
yzm_button.pack(padx=(0,60),pady=6)




frems2 = {"frem,_sjh":frem_sjh,"frem_mm":frem_mm,"frem_mm2":frem_mm2}
for i in frems2.values():
    i.pack(padx=0,pady=0)
frem_yzm.pack(padx=(60,0),pady=3)  # 单独放置验证码这一行

complter_and_fanhui = tk.Frame(frem2)
fanhui_button = tk.Button(complter_and_fanhui,
                          text="返回",
                          width=7,
                          command=lambda : show_frem(frem1))# 这是从注册页面返回到灯登录页面的一个按钮,变量名fanhui，意思是返回
fanhui_button.pack(side=tk.LEFT,padx=0,pady=0)
show_frem(frem1)  # 默认展示frem1也就是登录界面

def complted():
    if yzm_entry.get() == "" or mm_entry2.get() == "" or mm_entry == "" or sjh_entry.get() == "":
        print("请将信息填写完整")
        messagebox.showinfo("提示","请将信息填写完整")
    else:
        if yzm_entry.get() != sjs_jy:
            print("随机码错误")
            messagebox.showinfo("错误","随机码错误")
        else:
            print("随机码正确")
            messagebox.showinfo("正确","随机码正确")
            sql_zw = "insert into yx_and_mm(yx,mm)values(%s,%s);"
            cr.execute("use zhanghao;")
            cr.execute(sql_zw,(sjh_entry.get(),mm_entry.get()))
            print("打印存储结果")
            cr.execute("SELECT yx FROM yx_and_mm;")
            yx_column_vlaue = cr.fetchall()
            print(yx_column_vlaue)
            cr.execute("SELECT mm FROM yx_and_mm;")
            mm_column_vaslue = cr.fetchall()
            print(mm_column_vaslue)

complted_button = tk.Button(complter_and_fanhui,
                            text="确认",
                            width=7,
                            command= lambda :complted())
complted_button.pack(side=tk.LEFT,padx=0,pady=0)
complter_and_fanhui.pack(padx=0,pady=0)
root.mainloop()
print(sjs_jy)
print()
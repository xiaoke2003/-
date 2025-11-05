from pymysql import connect
class data:
    # 开始连接账号数据库
    con = connect(user="root", password="root", port=3306)
    cr = con.cursor()
    sql_index = 0
    data_list = ["create database zhanghao default character set utf8;",  # 执行ddl语句创建数据库
                "create table youxiang(yx varchar(20),mm varchar(20));",  # 创建表
                "alter table youxiang add column yx varchar(20), add column mm varchar(20);"  # 为空表添加列
                ]
    @classmethod
    def start_database(cls,my_tables,my_data_name:tuple):
        count_index = 0
        print("start_database类方法启动")
        start_loop = True
        while start_loop:
            for tuple_values in my_tables:
                print(f"show,text{tuple_values}")
                if my_data_name[coun  t_index] in tuple_values:
                    print(f"{my_data_name[count_index]}目标存在")
                    print(f"{my_data_name[count_index]}匹配值{tuple_values}")
                  else:
                    print(f"{my_data_name[count_index]}不存在，即将创建")
                    print(f"{my_data_name[count_index]}匹配值为{tuple_values}")
                    try:
                        cls.cr.execute(cls.data_list[count_index])
                    except:
                        print(f"{my_data_name[count_index]}创建失败")
                    else:
                        print(f"{my_data_name[count_index]}创建成功")
                count_index += 1
                if count_index == 2:
                    start_loop = False
if __name__ == "__main__":
    w = (("1212","333","555",),("1111","666",),("www","问问",),)
    a = data()
    c= ("333","1111","问问")
    use = a.start_database(w,c)





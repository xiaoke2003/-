from pymysql import connect
sql = connect(user="root",password="root",passwd=3306)
cr = sql.cursor()
def show_data(data_tuple,tar_name):
    tf = False
    for sun_tuple in data_tuple:
        if tar_name in sun_tuple:
            print(f"{tar_name}存在于{sun_tuple}")
            tf = True
            break

    if not tf:
        print(f"{tar_name}不存在\ntry_create")
        try:
            cr.execute(f"create database {tar_name} default character set utf8;")
            print(f"{tar_name}已创建")
            cr.execute(f"use {tar_name}")
            cr.execute("create table yx_and_mm(yx varchar(20),mm varchar(20);")  # 这里暂时先故意写死表和列，后续再开放
            print("数据结构搭建完成")
        except:
            print(f"{tar_name}创建失败了")
a = (('information_schema',), ('jizhang',), ('mysql',), ('performance_schema',), ('sys',), ('text',), ('text1',), ('text3',), ('wenyujie',), ('zhanghao',))
show_data(a,"111")
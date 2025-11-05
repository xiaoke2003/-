from pymysql import connect
con = connect(host="localhost",user="root",password="root",port=3306)
cr = con.cursor()
cr.execute("use wenyujie;")
cr.execute("select count(fenshu) from xiaojie;")
return_cr = cr.fetchall()
print(return_cr)
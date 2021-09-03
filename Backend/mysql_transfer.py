import mysql.connector

config = {
    'user': 'plant',
    'password': '',
    'host': '10.1.0.237',
    'database': 'plantiot',
    'port': '3306'
}
dbcon = mysql.connector.connect(**config)
cursor = dbcon.cursor()

add_test = ("INSERT INTO plant (id,name) VALUES (%s, %s) ")

data_test = (10,'testplant')

cursor.execute(add_test)
emp_no = cursor.lastrowid

dbcon.commit()

cursor.close()
dbcon.close()
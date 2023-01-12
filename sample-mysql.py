#pip install mysql-connector-python
import mysql.connector

cnx = mysql.connector.connect(
    user='root',
    password='1q2w3e4r5t',
    host='localhost',
    port='13306'
)
cursor = cnx.cursor()
cursor.execute('SELECT * FROM lec_db.users')

for id, name in cursor:
    print(f'{id}: {name}')

cursor.close()
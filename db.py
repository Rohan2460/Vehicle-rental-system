import mysql.connector

cnx = mysql.connector.connect(user="admin", password="password", host="localhost")
cursor = cnx.cursor()

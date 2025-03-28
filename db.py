import mysql.connector

cnx = mysql.connector.connect(user="admin", password="password", host="localhost")
cursor = cnx.cursor()
cursor.execute("USE vehicle_rental_db")
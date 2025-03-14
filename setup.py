from db import cursor, cnx

cursor.execute("CREATE DATABASE vehicle_rental_db")
cursor.execute("USE vehicle_rental_db")
cursor.execute("CREATE TABLE Customer (CustomerID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Email VARCHAR(255))")
cursor.execute("CREATE TABLE Bookings (BookingID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, BookingStatus VARCHAR(255), TotalAmount INT, CustomerID INT, FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID))")
cnx.commit()
# schema here 
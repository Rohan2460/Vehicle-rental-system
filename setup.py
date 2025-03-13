from db import cursor

cursor.execute("CREATE DATABASE vehicle_rental_db")
cursor.execute("USE vehicle_rental_db")
cursor.execute("CREATE TABLE Bookings (BookingID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, status VARCHAR(255))")
# schema here 
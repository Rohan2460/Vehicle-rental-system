from db import cursor, cnx
from models import *

tables = [Customer(), Employee(), Vehicle(), Booking(), Payments()]
for table in tables:
    table.create_table()

vehicle.create(model="Toyota Yaris", year=2009, availabilityStatus="available")
vehicle.create(model="Honda Amaze", year=2015, availabilityStatus="available")
employee.create(name="John", email="john@email.com", phone=123456789, role="Salesman")
employee.create(name="Mike", email="mike@email.com", phone=456789012, role="Salesman")

customer.create(name="Walter", email="walter@email.com", phone=453389012, licenseNumber="327 2153")

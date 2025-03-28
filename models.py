from orm import Table, Field

class Customer(Table):
    table_name = "Customer"
    customerID = Field(int, primary_key=True, auto_increment=True)
    name = Field(str)
    email = Field(str)
    phone = Field(int)
    licenseNumber = Field(str)


class Employee(Table):
    table_name = "Employees"
    employeeID = Field(int, primary_key=True, auto_increment=True)
    name = Field(str)
    email = Field(str)
    phone = Field(int)
    role = Field(str)


class Vehicle(Table):
    table_name = "Vehicle"
    vehicleID = Field(int, primary_key=True, auto_increment=True)
    model = Field(str)
    year = Field(int)
    availabilityStatus = Field(str)


class Booking(Table):
    table_name = "Bookings"
    bookingID = Field(int, primary_key=True, auto_increment=True)
    vehicleID = Field(int, foreign_key=Vehicle.vehicleID)
    bookingStartDate = Field(str)
    bookingEndDate = Field(str)
    employeeID = Field(int, foreign_key=Employee.employeeID)
    bookingStatus = Field(str)
    totalAmount = Field(int)
    customerID = Field(int, foreign_key=Customer.customerID)


class Payments(Table):
    table_name = "Payments"
    paymentID = Field(int, primary_key=True, auto_increment=True)
    bookingID = Field(int, foreign_key=Booking.bookingID)
    paymentDate = Field(str)
    paymentAmount = Field(int)

customer = Customer()
employee = Employee()
vehicle = Vehicle()
booking = Booking()
payments = Payments()
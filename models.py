from orm import Table, Field

class Customer(Table):
    table_name = "Customer"
    CustomerID = Field(int, primary_key=True, auto_increment=True)
    Name = Field(str)
    Email = Field(str)

class Booking(Table):
    table_name = "Bookings"
    BookingID = Field(int, max=10, primary_key=True, auto_increment=True)
    BookingStatus = Field(str)
    TotalAmount = Field(int)
    CustomerID = Field(int, Customer.CustomerID)

class Employee(Table):
    table_name = "Employee"
    EmployeeID = Field(int, max=10, primary_key=True, auto_increment=True)
    Name = Field(str)
    Email = Field(str)
    Phone = Field(int, max=10)
    booking = Field(int, max=10, foreign_key=Booking.BookingID)


customer = Customer()
booking = Booking()
# customer.create(Name="Mike", Email="mike@email.com")
# customer.update("name='John'", Email="johm@email.com")
employee = Employee()
employee.create_table()
print(customer.fetch())
print(booking.fetch(["BookingID"]))

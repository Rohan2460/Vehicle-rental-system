from db import cursor, cnx
from flask import Flask, flash, jsonify, render_template, request, redirect, url_for
from flask import session
from models import *


cursor.execute("USE vehicle_rental_db")
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['email']
        user = customer.fetch(condition=f"email='{mail}' AND name='{name}'")
        print(user)

        if user: 
            user = user[0]
            if user['name'] == name and user['email'] == mail:
                session.clear()
                session['username'] = user['name']
                return redirect(url_for('index'))

        return "Invalid"
            
    return '''
        <h1>LogIn</h1>
        <form method="post">
            <p>Name <input type=text name=name>
            <p>Email <input type=text name=email>
            <p><input type=submit value=Login>
        </form> <hr>
        <a href="/signup">Signup</a>
    '''

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['email']
        phone = request.form['phone']
        lic = request.form['lic']
        user = customer.fetch(condition=f"email='{mail}' AND name='{name}'")
        print(user)

        if not user: 
            customer.create(name=name, email=mail, phone=phone, licenseNumber=lic)
            session.clear()
            session['username'] = name
            return redirect(url_for('index'))
            
        return "Already exist / Error"
        
    return '''
        <h1>SignUp</h1>
        <form method="post">
            <p>Name <input type=text name=name>
            <p>Email <input type=text name=email>
            <p>Phone <input type=text name=phone>
            <p>License <input type=text name=lic>
            <p><input type=submit value=SignUp>
        </form> <hr>
        <a href="/login">Login</a>
    '''


@app.route("/")
def index():
    if not session:
        return redirect("/login")
    data = booking.raw_fetch(booking.fetch(return_as_txt=True) + f" JOIN Customer c ON Bookings.customerID = c.customerID WHERE c.name='{session['username']}' AND bookingStatus!='CLOSED' ", named=True)
    person = customer.fetch(condition=f"name='{session['username']}'")[0]
    emps = employee.fetch()
    veh = vehicle.fetch(condition="availabilityStatus='available'")
    return render_template("submit.html", data=data, customer=person, emp=emps, vehicle=veh)

@app.route("/data", methods=["POST"])
def get_data():
    if request.method == "POST":
        date_start = request.form["date_start"]
        date_end = request.form["date_end"]
        amount = request.form["amount"]
        status = request.form["status"]
        empId = request.form["employee"]
        vehicleId = request.form["vehicle"]
        c_id = request.form["c_id"]

        booking.create(vehicleID=vehicleId, bookingStartDate=date_start, 
                       bookingEndDate=date_end, employeeID=empId, 
                       bookingStatus=status, totalAmount=amount, customerID=c_id)
        vehicle.update(condition=f"vehicleID='{vehicleId}'", availabilityStatus="not available")

    return redirect("/")

@app.route("/manage")
def manage():

    table = vehicle.raw_fetch("""SELECT B.bookingID, B.bookingStatus, E.name, V.model, C.name, B.bookingStartDate FROM Bookings B 
                              JOIN Customer C ON C.customerID = B.customerID
                              JOIN Employees E ON E.employeeID = B.employeeID
                              JOIN Vehicle V ON V.vehicleID = B.vehicleID """, named=True, fields=["bookingID", "status", "employee", "vehicle", "customer", "date"])
    data = { "joined table": table, "vehicles" : vehicle.fetch(), "employees": employee.fetch(), "bookings": booking.fetch(), "customers": customer.fetch()}

    return render_template("manage.html", context=data)

@app.route("/close")
def set_data():
    id = request.args.get("id")
    booking.update(condition="bookingID=" + id, bookingStatus="CLOSED")
    v_id = booking.fetch(["vehicleID"], condition="bookingID=" + id)[0]["vehicleID"]
    vehicle.update(condition=f"vehicleID={v_id}", availabilityStatus="available")

    return redirect("/manage")

if __name__ == "__main__":
    app.run()
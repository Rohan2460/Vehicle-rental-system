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
        <form method="post">
            <p>Name <input type=text name=name>
            <p>Email <input type=text name=email>
            <p><input type=submit value=Login>
        </form>
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
        <form method="post">
            <p>Name <input type=text name=name>
            <p>Email <input type=text name=email>
            <p>Phone <input type=text name=phone>
            <p>License <input type=text name=lic>
            <p><input type=submit value=signup>
        </form>
    '''


@app.route("/")
def index():
    data = booking.raw_fetch(booking.fetch(return_as_txt=True) + f" b JOIN Customer c ON b.customerID = c.customerID WHERE name='{session['username']}'", named=True)
    person = customer.fetch(condition=f"name='{session['username']}'")[0]
    emps = employee.fetch()
    veh = vehicle.fetch()
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
                       bookingEndDate=date_start, employeeID=empId, 
                       bookingStatus=status, totalAmount=amount, customerID=c_id)

    return redirect("/")



if __name__ == "__main__":
    app.run()
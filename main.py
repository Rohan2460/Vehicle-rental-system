from db import cursor, cnx
from flask import Flask, jsonify, render_template, request, redirect

cursor.execute("USE vehicle_rental_db")
app = Flask(__name__)


@app.route("/")
def index():
    cursor.execute("SELECT * FROM Bookings")
    data = cursor.fetchall()
    # print(data)
    cursor.execute("SELECT Name FROM Customer WHERE CustomerID = 1")
    customer = cursor.fetchone()

    
    return render_template("submit.html", data=data, customer=customer[0])

@app.route("/data", methods=["POST"])
def get_data():
    if request.method == "POST":
        data = request.form["data"]
        amount = request.form["amount"]
        c_id = request.form["c_id"]

        cursor.execute(f"INSERT INTO Bookings (BookingStatus, TotalAmount, CustomerID) VALUES ('{data}', {amount}, {c_id})")
        cnx.commit()

    return redirect("/")


@app.route("/user", methods=["GET"])
def create_user():
    cursor.execute(f"INSERT INTO Customer (Name, Email) VALUES ('John', 'john@a.com')")
    cnx.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run()
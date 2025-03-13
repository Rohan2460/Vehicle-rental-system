from db import cursor
from flask import Flask, jsonify, render_template, request, redirect

cursor.execute("USE vehicle_rental_db")
app = Flask(__name__)


@app.route("/")
def index():
    cursor.execute("SELECT * FROM Bookings")
    data = cursor.fetchall()
    print(data)
    
    return render_template("submit.html", data=data)

@app.route("/data", methods=["POST"])
def get_data():
    if request.method == "POST":
        data = request.form["data"]
        cursor.execute(f"INSERT INTO Bookings (status) VALUES ('{data}')")

    return redirect("/")

if __name__ == "__main__":
    app.run()
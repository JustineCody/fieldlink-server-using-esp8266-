from flask import Flask, render_template, request, redirect, session, jsonify, url_for
import sqlite3
import random
from functools import wraps

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "your_secret_key_here"

def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# 🔐 Access control decorator
def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapped

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user and password == user["password"]:
            session["username"] = username
            return redirect("/dashboard")
        error = "Invalid login"
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except:
            return "Username already exists", 409
        finally:
            conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=session["username"])

@app.route("/sensor-data")
@login_required
def sensor_data():
    data = {
        "temperature": round(random.uniform(20.0, 30.0), 2),
        "humidity": round(random.uniform(40.0, 60.0), 2),
        "ph": round(random.uniform(6.5, 8.5), 2),
        "salinity": round(random.uniform(0.0, 35.0), 2)
    }
    return jsonify(data)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True, port=10000)

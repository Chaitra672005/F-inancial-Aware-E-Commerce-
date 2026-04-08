from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ---------------- DB SETUP ----------------
def get_db():
    return sqlite3.connect("database.db")

def init_db():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY,
        amount REAL,
        status TEXT
    )
    """)

    db.commit()
    db.close()

init_db()

# ---------------- FRAUD ENGINE ----------------
def calculate_risk(amount, hour, orders_last_hour):
    score = 0

    # Amount signal
    if amount > 50000:
        score += 40
    elif amount > 20000:
        score += 20

    # Time signal
    if hour < 6 or hour > 23:
        score += 30

    # Frequency signal
    if orders_last_hour > 3:
        score += 30

    if score >= 60:
        return "high", score
    elif score >= 30:
        return "medium", score
    return "low", score


# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return "Finance E-Commerce API Running 🚀"


# -------- AUTH --------
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO users(username, password) VALUES (?, ?)",
        (data["username"], data["password"])
    )

    db.commit()
    db.close()

    return {"message": "User registered"}


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    )

    user = cursor.fetchone()

    return {"success": bool(user)}


# -------- PRODUCTS --------
@app.route("/products")
def products():
    items = [
        {"id": 1, "name": "Phone", "price": 20000},
        {"id": 2, "name": "Laptop", "price": 60000},
        {"id": 3, "name": "Headphones", "price": 3000}
    ]
    return jsonify(items)


# -------- CHECKOUT + FRAUD --------
@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    amount = data["amount"]

    db = get_db()
    cursor = db.cursor()

    # Current hour
    hour = datetime.now().hour

    # Count orders (simple frequency)
    cursor.execute("SELECT COUNT(*) FROM orders")
    orders_last_hour = cursor.fetchone()[0]

    # Risk calculation
    risk_level, risk_score = calculate_risk(amount, hour, orders_last_hour)

    # Save order
    cursor.execute(
        "INSERT INTO orders(amount, status) VALUES (?, ?)",
        (amount, risk_level)
    )

    db.commit()
    db.close()

    return {
        "amount": amount,
        "risk_score": risk_score,
        "risk_level": risk_level
    }


# -------- EMI --------
@app.route("/emi")
def emi():
    P = float(request.args.get("amount"))
    r = float(request.args.get("rate")) / (12 * 100)
    n = int(request.args.get("months"))

    emi = (P * r * (1+r)**n) / ((1+r)**n - 1)

    return {"emi": round(emi, 2)}


# -------- TRANSACTIONS --------
@app.route("/transactions")
def transactions():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM orders")
    data = cursor.fetchall()

    return jsonify(data)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run()
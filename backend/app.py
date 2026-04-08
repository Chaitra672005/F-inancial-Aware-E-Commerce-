from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# DB setup
def get_db():
    return sqlite3.connect("database.db")

# init tables
def init_db():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY, amount REAL, status TEXT)")

    db.commit()
    db.close()

init_db()

# routes
@app.route("/")
def home():
    return "API Running 🚀"

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    db = get_db()
    cursor = db.cursor()

    cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", 
                   (data["username"], data["password"]))
    db.commit()
    db.close()

    return {"message": "User registered"}

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                   (data["username"], data["password"]))
    user = cursor.fetchone()

    return {"success": bool(user)}

@app.route("/products")
def products():
    items = [
        {"id": 1, "name": "Phone", "price": 20000},
        {"id": 2, "name": "Laptop", "price": 60000}
    ]
    return jsonify(items)

@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    total = data["amount"]

    flag = "Safe"
    if total > 50000:
        flag = "High Risk"

    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO orders(amount, status) VALUES (?, ?)", (total, flag))
    db.commit()
    db.close()

    return {"total": total, "fraud_flag": flag}

@app.route("/emi")
def emi():
    P = float(request.args.get("amount"))
    r = float(request.args.get("rate")) / (12 * 100)
    n = int(request.args.get("months"))

    emi = (P * r * (1+r)**n) / ((1+r)**n - 1)
    return {"emi": round(emi, 2)}

@app.route("/transactions")
def transactions():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM orders")
    data = cursor.fetchall()
    return jsonify(data)

if __name__ == "__main__":
    app.run()
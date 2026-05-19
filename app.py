from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = "shop.db"

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template("index.html", products=products)

@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = float(request.form["price"])
        stock = int(request.form["stock"])
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)",
                  (name, description, price, stock))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("add_product.html")

@app.route("/buy/<int:product_id>")
def buy(product_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Decrease stock by 1 if available
    c.execute("SELECT stock FROM products WHERE id=?", (product_id,))
    stock = c.fetchone()[0]
    if stock > 0:
        c.execute("UPDATE products SET stock=stock-1 WHERE id=?", (product_id,))
        conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
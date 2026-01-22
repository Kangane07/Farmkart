from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "farmkart_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:omkar07@localhost:5432/farmkart"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================= MODELS =================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))  # farmer / consumer


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    farmer_name = db.Column(db.String(100))


# ================= ROUTES =================

@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=request.form["password"],
            role=request.form["role"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            email=request.form["email"],
            password=request.form["password"]
        ).first()
        if user:
            session["user"] = user.name
            session["role"] = user.role
            session.setdefault("cart", [])
            return redirect("/dashboard")
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        product = Product(
            name=request.form["name"],
            price=request.form["price"],
            quantity=request.form["quantity"],
            farmer_name=session.get("user")
        )
        db.session.add(product)
        db.session.commit()
        return redirect("/")
    return render_template("add_product.html")


@app.route("/add_to_cart/<int:pid>")
def add_to_cart(pid):
    if session.get("role") != "consumer":
        return redirect("/")
    cart = session.get("cart", [])
    cart.append(pid)
    session["cart"] = cart
    return redirect("/cart")


@app.route("/cart")
def cart():
    cart_ids = session.get("cart", [])
    products = Product.query.filter(Product.id.in_(cart_ids)).all()
    return render_template("cart.html", products=products)


@app.route("/checkout")
def checkout():
    session.pop("cart", None)
    return render_template("checkout.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= MAIN =================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

import os
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from models import Product, User, db


def load_env_file(path=".env"):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


load_env_file()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///farmkart.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please login to continue.", "warning")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            if session.get("role") not in roles:
                flash("You are not authorized for this page.", "danger")
                return redirect(url_for("index"))
            return view_func(*args, **kwargs)

        return wrapped

    return decorator


@app.route("/")
def index():
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template("index.html", products=products)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "")

        if role not in {"farmer", "consumer"}:
            flash("Please select a valid role.", "warning")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for("login"))

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role,
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user"] = user.name
            session["role"] = user.role
            session.setdefault("cart", {})
            flash("Welcome back!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/add_product", methods=["GET", "POST"])
@login_required
@role_required("farmer")
def add_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        price = int(request.form.get("price", 0))
        quantity = int(request.form.get("quantity", 0))

        if price <= 0 or quantity <= 0:
            flash("Price and quantity must be greater than zero.", "warning")
            return redirect(url_for("add_product"))

        product = Product(
            name=name,
            price=price,
            quantity=quantity,
            farmer_name=session.get("user"),
        )
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully.", "success")
        return redirect(url_for("index"))

    return render_template("add_product.html")


@app.route("/add_to_cart/<int:pid>")
@login_required
@role_required("consumer")
def add_to_cart(pid):
    product = Product.query.get_or_404(pid)
    cart = session.get("cart", {})
    key = str(pid)

    current_qty = int(cart.get(key, 0))
    if current_qty >= product.quantity:
        flash("Cannot add more than available stock.", "warning")
        return redirect(url_for("index"))

    cart[key] = current_qty + 1
    session["cart"] = cart
    flash(f"Added {product.name} to cart.", "success")
    return redirect(url_for("cart"))


@app.route("/cart")
@login_required
@role_required("consumer")
def cart():
    cart_map = session.get("cart", {})
    product_ids = [int(pid) for pid in cart_map.keys()]
    products = Product.query.filter(Product.id.in_(product_ids)).all() if product_ids else []

    items = []
    total = 0
    for product in products:
        qty = int(cart_map.get(str(product.id), 0))
        subtotal = product.price * qty
        total += subtotal
        items.append({"product": product, "quantity": qty, "subtotal": subtotal})

    return render_template("cart.html", items=items, total=total)


@app.route("/checkout")
@login_required
@role_required("consumer")
def checkout():
    cart_map = session.get("cart", {})
    if not cart_map:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("cart"))

    for pid, qty in cart_map.items():
        product = Product.query.get(int(pid))
        if not product or product.quantity < int(qty):
            flash("Some items are out of stock. Please update your cart.", "danger")
            return redirect(url_for("cart"))

    for pid, qty in cart_map.items():
        product = Product.query.get(int(pid))
        product.quantity -= int(qty)

    db.session.commit()
    session["cart"] = {}
    return render_template("checkout.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

import os
from functools import wraps

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        if not os.path.exists(env_path):
            return False
        with open(env_path, "r", encoding="utf-8") as env_file:
            for line in env_file:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
        return False
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from models import Order, OrderItem, Product, User, db

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")


def build_default_postgres_url():
    pg_user = os.getenv("PGUSER", "postgres")
    pg_password = os.getenv("PGPASSWORD", "")
    pg_host = os.getenv("PGHOST", "localhost")
    pg_port = os.getenv("PGPORT", "5432")
    pg_db = os.getenv("PGDATABASE", "farmkart")

    if pg_password:
        return f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
    return f"postgresql://{pg_user}@{pg_host}:{pg_port}/{pg_db}"


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", build_default_postgres_url())
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def normalize_role(raw_role):
    return (raw_role or "").strip().lower()


def get_cart_dict():
    """Keep backward compatibility with older session cart format (list of ids)."""
    cart = session.get("cart", {})

    if isinstance(cart, dict):
        normalized = {}
        for product_id, qty in cart.items():
            try:
                product_key = str(int(product_id))
                normalized[product_key] = max(1, int(qty))
            except (TypeError, ValueError):
                continue
        return normalized

    if isinstance(cart, list):
        normalized = {}
        for product_id in cart:
            try:
                product_key = str(int(product_id))
            except (TypeError, ValueError):
                continue
            normalized[product_key] = normalized.get(product_key, 0) + 1
        return normalized

    return {}


def get_cart_count():
    return sum(get_cart_dict().values())


def verify_and_upgrade_password(user, entered_password):
    # Support legacy plain-text passwords and upgrade them to hash on successful login.
    if check_password_hash(user.password, entered_password):
        return True
    if user.password == entered_password:
        user.password = generate_password_hash(entered_password)
        db.session.commit()
        return True
    return False


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped_view


def role_required(*allowed_roles):
    allowed = {normalize_role(role) for role in allowed_roles}

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if not session.get("user_id"):
                flash("Please log in to continue.", "warning")
                return redirect(url_for("login"))
            if normalize_role(session.get("role")) not in allowed:
                flash("You are not authorized to access this page.", "danger")
                return redirect(url_for("index"))
            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator


@app.context_processor
def inject_global_template_data():
    return {"cart_count": get_cart_count()}


@app.route("/")
def index():
    query_text = request.args.get("q", "").strip()
    product_query = Product.query

    if query_text:
        like_pattern = f"%{query_text}%"
        product_query = product_query.filter(Product.name.ilike(like_pattern))

    products = product_query.order_by(Product.id.desc()).all()
    return render_template("index.html", products=products, query_text=query_text)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        role = normalize_role(request.form["role"])
        if role not in {"farmer", "consumer"}:
            flash("Please choose a valid role.", "warning")
            return redirect(url_for("register"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email is already registered. Please log in.", "warning")
            return redirect(url_for("login"))

        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if not user or not verify_and_upgrade_password(user, password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        session["user_id"] = user.id
        session["user"] = user.name
        session["role"] = normalize_role(user.role)
        session["cart"] = get_cart_dict()
        session.modified = True

        flash("Logged in successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    farmer_products = []
    if normalize_role(session.get("role")) == "farmer":
        farmer_products = (
            Product.query.filter_by(farmer_name=session.get("user", ""))
            .order_by(Product.id.desc())
            .all()
        )
    return render_template("dashboard.html", farmer_products=farmer_products)


@app.route("/add_product", methods=["GET", "POST"])
@role_required("farmer")
def add_product():
    if request.method == "POST":
        product = Product(
            name=request.form["name"].strip(),
            price=int(request.form["price"]),
            quantity=int(request.form["quantity"]),
            farmer_name=session.get("user", "Unknown"),
        )
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully.", "success")
        return redirect(url_for("index"))

    return render_template("add_product.html")


@app.route("/add_to_cart/<int:pid>", methods=["POST"])
@role_required("consumer")
def add_to_cart(pid):
    product = Product.query.get_or_404(pid)
    cart = get_cart_dict()
    key = str(pid)
    current_qty = int(cart.get(key, 0))

    if current_qty >= product.quantity:
        flash(f"Only {product.quantity} unit(s) of {product.name} available.", "warning")
        return redirect(url_for("index"))

    cart[key] = current_qty + 1
    session["cart"] = cart
    session.modified = True
    flash(f"{product.name} added to cart.", "success")
    return redirect(url_for("index"))


@app.route("/update_cart/<int:pid>", methods=["POST"])
@role_required("consumer")
def update_cart(pid):
    action = request.form.get("action")
    cart = get_cart_dict()
    key = str(pid)

    if key not in cart:
        return redirect(url_for("cart"))

    product = Product.query.get_or_404(pid)
    qty = int(cart.get(key, 0))

    if action == "inc" and qty < product.quantity:
        cart[key] = qty + 1
    elif action == "dec":
        if qty <= 1:
            cart.pop(key, None)
        else:
            cart[key] = qty - 1
    elif action == "remove":
        cart.pop(key, None)

    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart"))


@app.route("/cart")
@role_required("consumer")
def cart():
    cart_data = get_cart_dict()
    cart_items = []
    total = 0

    for product_id_str, qty in cart_data.items():
        product = Product.query.get(int(product_id_str))
        if not product:
            continue

        quantity = min(max(0, int(qty)), product.quantity)
        if quantity <= 0:
            continue
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    session["cart"] = {str(item["product"].id): item["quantity"] for item in cart_items}
    session.modified = True
    return render_template("cart.html", cart_items=cart_items, total=total)


@app.route("/checkout", methods=["POST"])
@role_required("consumer")
def checkout():
    cart_data = get_cart_dict()
    if not cart_data:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("cart"))

    updates = []
    for product_id_str, qty in cart_data.items():
        product = Product.query.get(int(product_id_str))
        if not product:
            flash("A cart item is no longer available.", "danger")
            return redirect(url_for("cart"))
        if int(qty) > product.quantity:
            flash(f"Insufficient stock for {product.name}.", "danger")
            return redirect(url_for("cart"))
        updates.append((product, int(qty)))

    order_total = 0
    order = Order(user_id=session["user_id"], total_amount=0)
    db.session.add(order)
    db.session.flush()

    for product, qty in updates:
        product.quantity -= qty
        subtotal = product.price * qty
        order_total += subtotal
        db.session.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                unit_price=product.price,
                quantity=qty,
                subtotal=subtotal,
            )
        )

    order.total_amount = order_total

    db.session.commit()
    session["cart"] = {}
    session.modified = True
    flash("Order placed successfully.", "success")
    return render_template("checkout.html", order=order)


@app.route("/orders")
@role_required("consumer")
def orders():
    user_orders = (
        Order.query.filter_by(user_id=session["user_id"])
        .order_by(Order.id.desc())
        .all()
    )
    return render_template("orders.html", orders=user_orders)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

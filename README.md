# FarmKart

FarmKart is a role-based online marketplace that connects **farmers** and **consumers**. Farmers can list products, and consumers can browse, add items to cart, and place orders.

## ✨ Features

- User registration and login with secure password hashing
- Role-based permissions:
  - **Farmer**: add/manage products
  - **Consumer**: browse products, manage cart, checkout
- Session-based shopping cart with quantity handling
- Checkout with stock validation and inventory updates
- Order history with itemized order details
- Flash messages for better user feedback
- Responsive marketplace-style UI
- Environment-based configuration via `.env`
- Legacy compatibility helpers for old password/cart formats

## 🧰 Tech Stack

### Frontend
- HTML (Jinja templates)
- CSS
- Flask templating engine (server-rendered views)

### Backend
- Flask (Python web framework)
- Flask-SQLAlchemy (ORM)
- Session management via Flask session

### Database
- PostgreSQL (recommended for production)
- SQLite (supported for local development)

### Languages Used
- Python
- HTML
- CSS
- SQL (via SQLAlchemy/database engine)

## 📁 Project Structure (high-level)

- `app.py` — main Flask application and routes
- `models.py` — SQLAlchemy models and relationships
- `templates/` — frontend pages (Jinja + HTML)
- `static/css/style.css` — styling
- `requirements.txt` — Python dependencies

## 🚀 Getting Started

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` from `.env.example` and add your values:

```env
SECRET_KEY=your-secret
DATABASE_URL=postgresql://username:password@localhost:5432/farmkart
```

For local SQLite usage:

```env
DATABASE_URL=sqlite:///farmkart.db
```

4. Run the app:

```bash
python app.py
```

## ✅ Current Implemented Scope

- Authentication flow (register/login/logout)
- Password hashing and validation
- Product creation by farmers
- Product listing and search-style browsing
- Cart operations with quantity and totals
- Checkout flow with stock reduction
- Order history for users

## 📌 Notes

- Keep `.env` private and never commit secrets.
- Use PostgreSQL for production workloads.
- Legacy user/cart compatibility code is included to avoid data breaks.

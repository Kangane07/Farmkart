# FarmKart

FarmKart is a Flask marketplace app connecting farmers and consumers.

## Implemented Scope

- User registration and login with hashed passwords.
- Login validation and user-facing flash messages.
- Role-based access guards:
  - Farmers can add products.
  - Consumers can add items to cart and checkout.
- Session cart with quantity support, per-item subtotal, and grand total.
- Checkout stock validation and inventory reduction after purchase.
- Persistent order history (`My Orders`) with order items and totals.
- Environment-based configuration using `.env`.
- SQLAlchemy models centralized in `models.py`.
- Marketplace-style responsive frontend (search bar, product grid, cart summary, farmer listing table).
- Backward compatibility fixes for legacy data:
  - old plain-text user passwords are upgraded to hashes after successful login.
  - old cart session format (list) is auto-converted to quantity map.

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL or SQLite

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment template and fill values:

```bash
copy .env.example .env
```

4. Update `.env`:

```env
SECRET_KEY=your-secret
DATABASE_URL=postgresql://username:password@localhost:5432/farmkart
```

You can also use SQLite locally:

```env
DATABASE_URL=sqlite:///farmkart.db
```

5. Run the app:

```bash
python app.py
```

## Notes

- Keep `.env` private. It is excluded by `.gitignore`.
- If moving from plain-text passwords, existing user records should be recreated or migrated.

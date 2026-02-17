# 🌾 FarmKart
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

FarmKart is a full-stack web application developed as a college project.
It connects farmers directly with consumers, allowing the sale of fresh vegetables and fruits without middlemen.

The project demonstrates frontend, backend, authentication, and database integration concepts using Python and Flask.

---

## 📌 Project Description

FarmKart provides a simple digital marketplace where:

- Farmers can register and add products
- Consumers can browse products and add items to cart
- Consumers can checkout and place a basic purchase

This project focuses on clarity, simplicity, and real-world applicability.

---

## 🧩 Features (Current Scope)

- User registration/login with Farmer & Consumer roles
- Password hashing for secure login storage
- Role-based route protection
- Product management by farmers
- Product browsing for consumers
- Cart with quantity tracking and total amount
- Basic checkout flow with stock reduction
- Clean and simple UI with dark mode

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- Flask-SQLAlchemy

### Frontend
- HTML
- CSS
- JavaScript

### Database
- SQLite (default for local setup)
- PostgreSQL (optional via `DATABASE_URL`)

### Tools
- VS Code
- GitHub

---

## 📂 Project Structure

FarmKart/
│── app.py
│── models.py
│── requirements.txt
│── .env.example
│── static/
│   └── css/
│       └── style.css
│── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── add_product.html
│   ├── cart.html
│   └── checkout.html

---

## ▶️ How to Run the Project Locally

1. Clone the repository
2. Open the project folder
3. Create and activate a virtual environment
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create environment file from sample:
   ```bash
   cp .env.example .env
   ```
6. Run the Flask app:
   ```bash
   python app.py
   ```
7. Open:
   `http://127.0.0.1:5000/`

---

## 🔐 Configuration

The app reads secrets from environment variables:

- `SECRET_KEY` - Flask session key
- `DATABASE_URL` - SQLAlchemy database URL

Default in `.env.example` uses SQLite for easy local setup.

---

## 🌐 Deployment Note

This project uses Flask, which is a server-side framework.

- GitHub Pages supports only static websites (HTML, CSS, JS)
- Therefore Flask backend cannot run directly on GitHub Pages

For demonstration, deploy on Render, PythonAnywhere, or run locally.

---

## 🎓 Academic Purpose

This project was developed as part of a college curriculum to:
- Understand full-stack web development
- Learn Flask framework
- Practice authentication and role-based access
- Apply database and MVC concepts

---

## 👤 Author

**Omkar Kangane**
College Project – FarmKart

---

## 📄 License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

---

## 📁 Project Documentation

- Project PPT available in `/docs`
- Screenshots of the application in `/docs/screenshots`

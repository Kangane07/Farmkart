# 🌾 FarmKart
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Status](https://img.shields.io/badge/Project-College%20Project-orange)

FarmKart is a full-stack web application developed as a college project.  
It connects farmers directly with consumers, allowing the sale of fresh vegetables and fruits without middlemen.

The project demonstrates the integration of frontend, backend, and database concepts using Python and Flask.

---

## 📌 Project Description

FarmKart aims to solve the problem of intermediaries between farmers and consumers by providing a simple digital platform where:

- Farmers can add and manage their products
- Customers can browse products and place orders
- Orders are handled in a structured and organized manner

This project focuses on clarity, simplicity, and real-world applicability.

---

## 🧩 Features

- User authentication (Farmer & Customer roles)
- Product management by farmers
- Product browsing for customers
- Cart and checkout system
- Order management
- Clean and simple UI

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask

### Frontend
- HTML
- CSS
- JavaScript

### Database
- SQLite

### Tools
- VS Code
- GitHub

---

## 📂 Project Structure

FarmKart/
│── app.py
│── models.py
│── requirements.txt
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

## 📊 Database Design (ER Diagram)

The database design is based on the following entities:

### Entities
- **User** (Farmer / Customer)
- **Product**
- **Order**
- **OrderItem**

### Relationships
- A user (farmer) can add multiple products
- A customer can place multiple orders
- An order can contain multiple products

The ER diagram visually represents these relationships and was created as part of the project documentation.

---

## ▶️ How to Run the Project Locally

1. Clone or download the repository
2. Open the project folder in VS Code
3. Create and activate a virtual environment
4. Install required dependencies:
pip install -r requirements.txt
5. Run the Flask application:
python app.py
6. Open your browser and visit:
http://127.0.0.1:5000/

---

## 🌐 Deployment Note

This project uses Flask, which is a server-side framework.

- GitHub Pages supports only static websites (HTML, CSS, JS)
- Therefore, the Flask backend cannot be run directly on GitHub Pages

For demonstration purposes, the project can be:
- Run locally, or
- Deployed on platforms like Render or PythonAnywhere

---

## 🎓 Academic Purpose

This project was developed as part of a college curriculum to:
- Understand full-stack web development
- Learn Flask framework
- Practice database modeling and ER diagrams
- Apply MVC architecture concepts

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
- ER Diagram included in `/docs`

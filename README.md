# 🚗 Car Rental Management System

A full‑stack web application to automate and manage vehicle rental operations for customers and rental agencies.

---

## 📌 Project Overview

The Car Rental Management System streamlines the complete rental lifecycle — from browsing cars and booking online to managing returns and payments. It replaces manual processes with a digital platform that improves efficiency, accuracy, and customer experience.

---

## ✨ Key Features

### 👤 Customer

* User registration & secure login
* Browse cars by category, price, availability
* Real‑time availability checking
* Online booking & reservation
* Rental history tracking
* Profile management

### 🛠️ Admin

* Add / update / delete cars
* Manage pricing & categories
* View and manage bookings
* Track rentals & returns
* Payment monitoring
* Dashboard & reports

---

## 🧱 Tech Stack

### 💻 Backend

* Python
* Flask (API framework)
* SQLAlchemy (ORM)

### 🌐 Frontend

* HTML5
* CSS3
* JavaScript (Vanilla)

### 🗄️ Databases

* SQL (SQLite / MySQL / PostgreSQL) — structured data
* MongoDB — metadata, logs, cache

---

## 📁 Project Structure

```
car-rental-system/
│
├── backend/
│   ├── run.py
│   ├── config.py
│   ├── requirements.txt
│   └── app/
│       ├── models/
│       ├── routes/
│       ├── services/
│       └── utils/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
│
├── database/
│   ├── sql/
│   └── mongodb/
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/car-rental-system.git
cd car-rental-system/backend
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start MongoDB

```bash
mongod
```

### 5️⃣ Run Backend Server

```bash
python run.py
```

Server runs at:

```
http://127.0.0.1:5000
```

### 6️⃣ Run Frontend

Open:

```
frontend/index.html
```

(Use VS Code Live Server recommended)

---

## 🔌 API Endpoints (Sample)

### Auth

* `POST /api/register`
* `POST /api/login`

### Cars

* `GET /api/cars`
* `POST /api/cars`

### Booking

* `POST /api/book`

### Admin

* `GET /api/admin/bookings`
* `PUT /api/admin/car/<id>/return`

---

## 🗄️ Database Design

### SQL Tables

* users
* cars
* bookings
* payments
* rentals

### MongoDB Collections

* car_metadata
* activity_logs
* search_cache

---

## 🚀 Future Enhancements

* JWT Authentication
* Online Payment Gateway
* Admin Analytics Dashboard
* Email & SMS Notifications
* Car Image Uploads
* Deployment (AWS / Render)

---

## 👨‍💻 Author

**Vijay Kumar**

---

## 📜 License

This project is for educational and demonstration purposes.

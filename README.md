# 🏨 Hotel Room Booking API (FastAPI Project)

This project is a backend application built using FastAPI that simulates how a hotel manages its rooms and guest bookings.
It covers everything from basic room listing to booking management, check-in/check-out operations, and advanced features like search, sorting, and pagination.

The main goal of this project was to understand how APIs work in real-world systems and how different features can be combined to build a complete backend service.

---

## ✨ What This Project Does

* Keeps track of hotel rooms and their availability
* Allows users to book rooms for a number of nights
* Calculates total cost based on stay and selected meal plan
* Supports early checkout with discount
* Handles check-in and check-out operations
* Provides search, filter, sort, and pagination functionalities

---

## 🧠 Key Features Explained

### 🛏️ Room Management

* View all rooms with details like type, floor, and price
* Add new rooms (with duplicate validation)
* Update room price or availability
* Delete rooms (only if not occupied)

---

### 📖 Booking System

* Create bookings with validation (name, nights, phone, etc.)
* Prevent booking of already occupied rooms
* Automatically update room availability after booking
* Calculate total cost including meal plans:

  * `none` → no extra cost
  * `breakfast` → ₹500/night
  * `all-inclusive` → ₹1200/night

---

### 🔄 Check-in & Check-out

* Check-in updates booking status
* Check-out updates booking status and frees the room
* Track active bookings (confirmed + checked-in)

---

### 🔍 Search & Filtering

* Search rooms using keyword (room number or type)
* Filter rooms based on:

  * type
  * price
  * floor
  * availability

---

### 📊 Sorting & Pagination

* Sort rooms by price, floor, or type
* Sort bookings by cost or nights
* Paginate results to view data page-wise
* Combined browsing feature (search + sort + pagination together)

---

## ⚙️ Technologies Used

* **Python** — core programming language
* **FastAPI** — API framework
* **Pydantic** — request validation
* **Uvicorn** — ASGI server

---

## 📁 Project Structure

```
project/
│
├── main.py        # All API routes and logic
├── README.md      # Project documentation
```

---

## ▶️ How to Run This Project

Follow these steps to run the project locally:

### 1. Create a virtual environment

```
python -m venv venv
```

### 2. Activate it

* Windows:

```
venv\Scripts\activate
```

* Mac/Linux:

```
source venv/bin/activate
```

### 3. Install required packages

```
pip install fastapi uvicorn
```

### 4. Start the server

```
uvicorn main:app --reload
```

### 5. Open API docs

```
http://127.0.0.1:8000/docs
```

Swagger UI will allow you to test all endpoints easily.

---

## ⚠️ Important Notes

* This project uses in-memory data (no database), so all data resets when the server restarts
* Route order matters in FastAPI — fixed routes must be written above dynamic routes
* Validation errors are automatically handled using Pydantic

---

## 🧩 Concepts Covered

This project helped in understanding:

* REST API design
* Path and query parameters
* Request body validation
* Helper functions for cleaner code
* CRUD operations
* Business logic implementation
* Search, filtering, sorting, pagination
* Handling edge cases and errors

---

## 📌 Example Endpoints

* `GET /rooms` → list all rooms
* `POST /bookings` → create a booking
* `POST /checkin/{booking_id}` → check-in
* `POST /checkout/{booking_id}` → check-out
* `GET /rooms/search` → search rooms
* `GET /rooms/browse` → combined filtering + sorting + pagination

---

## 💡 Learning Outcome

Building this project gave practical experience in designing APIs from scratch.
It also improved understanding of how backend systems handle user requests, manage data, and apply business rules.

---


## 🙌 Acknowledgment

This project was built as part of a learning journey to explore FastAPI and backend development concepts.

---


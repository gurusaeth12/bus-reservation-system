# 🚌 Bus Reservation System Using Python

A simple Bus Reservation System developed using Python Tkinter and SQLite. The application provides a graphical interface for booking bus tickets, searching bookings, cancelling bookings, and viewing all reservations.

## 📌 Project Overview

The Bus Reservation System is a desktop-based application designed to manage bus ticket reservations.

The system uses a graphical user interface built with Tkinter and stores booking information in an SQLite database. Users can select a bus, choose an available seat, make a booking, search for existing bookings, cancel reservations, and view all bookings.

## ✨ Features

- 🚌 Bus selection
- 🎟️ Ticket booking
- 💺 Available seat selection
- 🔍 Search booking
- ❌ Cancel booking
- 📋 View all bookings
- 💾 SQLite database storage
- 🖥️ User-friendly graphical interface
- ⚠️ Input validation
- 🔄 Automatic seat availability checking

## 🛠️ Technologies Used

- Python
- Tkinter
- SQLite
- SQL
- Python SQLite3 module

## 🏗️ System Architecture

              ┌──────────────────────┐
              │   Tkinter GUI        │
              └──────────┬───────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      Book Ticket   Search Booking   Cancel Booking
          │              │              │
          └──────────────┼──────────────┘
                         ▼
              ┌──────────────────────┐
              │   SQLite Database    │
              │ bus_reservation.db   │
              └──────────────────────┘
              
## ⚙️ How It Works

1. The application starts with the main menu.
2. The user can choose to book, search, cancel, or view bookings.
3. During booking, the user enters their name and selects a bus.
4. The system checks the SQLite database for already booked seats.
5. Only available seats are displayed.
6. The booking information is stored in the SQLite database.
7. Users can search their booking using their name or bus.
8. Existing bookings can also be cancelled.
9. All stored bookings can be displayed using the View All Bookings option.

## 💺 Available Buses and Seats

### Bus 1

* A1
* A2
* A3
* A4

### Bus 2

* B1
* B2
* B3
* B4

The system automatically removes already booked seats from the available seat list.

## 📂 Project Structure

BUS-RESERVATION-SYSTEM-USING-PYTHON
│
├── BusReservationSystem
│   ├── busreservation main.py
│   ├── bus_reservation.db
│   └── portfolio.db
│
└── README.md

## 🚀 How to Run

### Step 1: Install Python

Make sure Python is installed on your computer.

Check the installation using:

python --version

### Step 2: Clone the Repository

git clone https://github.com/gurusaeth12/BUS-RESERVATION-SYSTEM-USING-PYTHON.git

### Step 3: Open the Project Folder

Navigate to the project directory:

cd BUS-RESERVATION-SYSTEM-USING-PYTHON

### Step 4: Run the Application

Run the Python file:

python "busreservation main.py"

The Bus Reservation System window will open.

## 📸 Project Preview

[Bus Reservation System](screenshot.png)

## 🎯 Learning Outcomes

Through this project, the following concepts were practiced:

* Python programming
* GUI development using Tkinter
* Database management using SQLite
* SQL queries
* CRUD operations
* Event-driven programming
* Input validation
* User interface design

## 🔮 Future Improvements

* Add more buses and routes
* Add passenger contact details
* Add date and time selection
* Add seat layout visualization
* Generate digital tickets
* Add admin login
* Add payment integration
* Export booking details
* Improve database structure

## 👨‍💻 Author

**Gurusaeth**

GitHub: [https://github.com/gurusaeth12](https://github.com/gurusaeth12)

⭐ If you find this project useful, consider giving the repository a star.

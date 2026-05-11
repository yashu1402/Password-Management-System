# 🔐 Password Management System

A secure **Password Management System** built with **Python** and **MySQL**.  
This project allows users to store, manage, and retrieve their account credentials safely with a simple interface.

---

## 📌 Features
- **Add New Passwords**: Save credentials for websites, apps, or services.
- **Retrieve Passwords**: Quickly fetch stored credentials when needed.
- **Update/Delete Entries**: Modify or remove saved records.
- **Search Functionality**: Find accounts easily by name.
- **Encryption Support** *(optional)*: Securely store passwords using hashing/encryption.

---

## 🛠️ Tech Stack
- **Language**: Python
- **Database**: MySQL
- **Libraries**:
  - Tkinter (GUI interface)
  - PyMySQL / mysql-connector-python (database connectivity)
  - Cryptography (for encryption, if enabled)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x installed
- MySQL server installed and running
- Git (for cloning the repository)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yashu1402/Password-Management-System.git
   cd Password-Management-System

---

### Install dependencies:
- pip install -r requirements.txt

---

### Configure database:
- Create a new MySQL database
  (e.g.,password_db).
- Update config.py with your MySQL
  credentials (host, user, password,
  database).
- Run the provided SQL script to set up
  tables.

---

### Run the application:
- python main.py

---

### Project Structure
Password-Management-System/
│── main.py               # Entry point

│── config.py             # Database configuration

│── database.py           # MySQL setup and queries

│── gui.py                # Tkinter GUI components

│── utils.py              # Helper functions (encryption, validation)

│── requirements.txt      # Dependencies

│── README.md             # Documentation

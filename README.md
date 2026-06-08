<!-- <div align="center">

# 💸 Expense Tracker Lite

**A clean, fast, self-hosted expense tracker built with Flask and SQLite.**  
Log your daily spending, visualize patterns with live charts, and export data — all in a dark, minimal UI.

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.3-000000?style=flat-square&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-CDN-38BDF8?style=flat-square&logo=tailwindcss&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## Overview

Expense Tracker Lite is a single-user, browser-based personal finance tool. It stores every expense in a local SQLite database, requires no external services or cloud accounts, and runs entirely on your machine. The dashboard combines a filterable transaction table with real-time Chart.js visualizations so you can see where your money goes at a glance.

---

## Features

| Feature | Details |
|---|---|
| ➕ **Add Expenses** | Record description, amount (₹), category, and date |
| 🔍 **Smart Filtering** | Filter the dashboard by date range, category, or both simultaneously |
| ✏️ **Inline Editing** | Update any field of a saved expense via a dedicated edit form |
| 🗑️ **Safe Deletion** | Remove individual records with a single POST action |
| 🥧 **Pie Chart** | Category-wise spending breakdown, filtered in real time |
| 📊 **Bar Chart** | Day-by-day spending trend across your selected date range |
| 📥 **CSV Export** | Download your filtered dataset; filename includes the date range automatically |
| 🔔 **Flash Notifications** | Contextual success and error messages for every action |
| 🌑 **Dark UI** | Tailwind CSS dark theme (`zinc-950` / `slate-900`) with a brand accent color |

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.8+ |
| Web Framework | Flask | 3.1.3 |
| ORM | Flask-SQLAlchemy / SQLAlchemy | 3.1.1 / 2.0.50 |
| Database | SQLite | (built-in, via Flask) |
| Templating | Jinja2 | 3.1.6 |
| Styling | Tailwind CSS | CDN |
| Charts | Chart.js | CDN |
| WSGI Toolkit | Werkzeug | 3.1.8 |

---

## Project Structure

```
Expense_Tracker-main/
│
├── app.py                  # Application entry point — routes, models, business logic
├── requirements.txt        # Pinned Python dependencies
├── .gitignore              # Excludes instance/, __pycache__, .vscode/
│
└── templates/
    ├── base.html           # Shared layout — header, footer, flash message block
    ├── index.html          # Main dashboard — filters, add form, table, charts
    ├── index1.html         # Alternate dashboard layout
    └── edit.html           # Edit expense form (pre-populated fields)
```

> The `instance/` directory and `my_database.db` are created automatically on first run and are excluded from version control.

---

## Data Model

```python
class Expense(db.Model):
    id          : Integer   (primary key, auto-increment)
    description : String    (max 120 chars, required)
    amount      : Float     (required, must be > 0)
    category    : String    (max 20 chars, required)
    date        : Date      (required, defaults to today)
```

### Supported Categories

`Food` · `Transport` · `Health` · `Rent` · `Utilities`

---

## API Routes

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Dashboard — filterable expense list + charts |
| `POST` | `/add` | Create a new expense record |
| `POST` | `/delete/<int:id>` | Delete an expense by ID |
| `GET` | `/edit/<int:exp_id>` | Render the edit form for an expense |
| `POST` | `/edit_record/<int:id>` | Persist edited expense data |
| `GET` | `/export_csv` | Stream filtered expenses as a downloadable CSV |

### Filter Query Parameters (on `GET /`)

| Parameter | Type | Description |
|---|---|---|
| `start` | `YYYY-MM-DD` | Filter expenses on or after this date |
| `end` | `YYYY-MM-DD` | Filter expenses on or before this date |
| `category` | string | Limit results to a specific category |

---

## CSV Export Format

The export respects the current filter state. The downloaded file is named:

```
Expenses_<start>_to_<end>.csv
```

Example: `Expenses_2026-01-01_to_2026-06-06.csv`

**Columns:** `Id`, `Date` (DD-MM-YYYY), `Description`, `Category`, `Amount`

---

## Getting Started

### Prerequisites

- Python **3.8** or higher
- `pip`

### Installation

**1. Clone or extract the repository**

```bash
git clone <your-repo-url>
cd Expense_Tracker-main
```

**2. Create and activate a virtual environment**

```bash
# Create
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the development server**

```bash
python app.py
```

**5. Open in your browser**

```
http://127.0.0.1:5000
```

The SQLite database is created automatically at `instance/my_database.db` on first launch. No migrations or setup commands are required.

---

## Dependencies

```text
blinker==1.9.0
click==8.4.1
colorama==0.4.6
Flask==3.1.3
Flask-SQLAlchemy==3.1.1
greenlet==3.5.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
SQLAlchemy==2.0.50
typing_extensions==4.15.0
Werkzeug==3.1.8
```

---

## Security Notes

> These apply before deploying outside a local machine.

- **Debug mode** — `app.run(debug=True)` is set in `app.py`. **Disable this in production** by setting `debug=False` or using a production WSGI server such as Gunicorn.
- **Secret key** — The `SECRET_KEY` is hardcoded. Replace it with a strong, randomly generated value before any non-local deployment:
  ```python
  import secrets
  print(secrets.token_hex(32))
  ```
- **Single-user** — There is no authentication layer. Do not expose this application to a public network without adding one.

---

## License

This project is released under the [MIT License](LICENSE).-->

<div align="center">
💸 Expense Tracker Lite

A modern, secure, self-hosted expense tracker built with Flask, SQLite, and user authentication.
Track daily expenses, visualize spending patterns, and manage your finances with a clean dark UI.

</div>
Overview

Expense Tracker Lite is now a multi-user Flask web application with authentication support.
Each user has a secure, isolated expense dashboard backed by SQLite.

Key improvements include:

Secure user registration & login system
Password hashing using bcrypt
Session-based authentication
Protected routes (dashboard accessible only after login)
Flash messaging for better UX feedback
Features
Feature	Details
👤 User Authentication	Register, login, logout with session handling
🔐 Secure Passwords	Passwords hashed using bcrypt
➕ Add Expenses	Record description, amount, category, and date
🔍 Smart Filtering	Filter by date range and category
✏️ Edit Expenses	Update saved records via dedicated form
🗑️ Delete Expenses	Safe POST-based deletion
🥧 Pie Chart	Category-wise spending breakdown
📊 Bar Chart	Daily spending trends
📥 CSV Export	Download filtered data instantly
🔔 Flash Messages	Success & error feedback for actions
🌑 Dark UI	Tailwind-based modern dark theme
Tech Stack
Layer	Technology
Backend	Flask
Auth	Flask sessions + bcrypt
Database	SQLite
ORM	SQLAlchemy
Frontend	Jinja2 + Tailwind CSS
Charts	Chart.js
Server	Werkzeug
Project Structure
Expense_Tracker/
│
├── app.py                  # Routes, auth logic, models
├── requirements.txt
├── .gitignore
│
└── templates/
    ├── base.html
    ├── login.html         # 🔐 Login page
    ├── register.html      # 🆕 Registration page
    ├── index.html         # Dashboard (protected)
    ├── edit.html

SQLite database is auto-created inside instance/my_database.db

Authentication Flow (NEW)
Registration
User creates account (username + password)
Password is hashed using bcrypt before storage
Login
Password is verified using bcrypt check
On success → session is created → redirected to dashboard
Logout
Session cleared
User redirected to login page
Security Notes
Protected routes require login
Direct access to / redirects to login if not authenticated
Data Model
class User(db.Model):
    id       : Integer (PK)
    username : String (unique)
    password : String (bcrypt hashed)


class Expense(db.Model):
    id          : Integer (PK)
    user_id     : Integer (FK → User.id)
    description : String
    amount      : Float
    category    : String
    date        : Date
API Routes
Method	Endpoint	Description
GET/POST	/register	Create new user
GET/POST	/login	User login
GET	/logout	End session
GET	/	Dashboard (protected)
POST	/add	Add expense
GET	/edit/<id>	Edit form
POST	/edit_record/<id>	Update expense
POST	/delete/<id>	Delete expense
GET	/export_csv	Download filtered CSV
CSV Export

Exports only the logged-in user's filtered data.

Filename format:

Expenses_<start>_to_<end>.csv
Getting Started
1. Clone repository
git clone <your-repo-url>
cd Expense_Tracker
2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3. Install dependencies
pip install -r requirements.txt
4. Run application
python app.py
5. Open in browser
http://127.0.0.1:5000
Dependencies
Flask
Flask-SQLAlchemy
bcrypt
Jinja2
bcrypt
Important Notes (Production)
❗ debug=True should be disabled in production
🔑 Replace hardcoded SECRET_KEY with secure random value
🔐 Never expose app without authentication layer (already added)
🧠 Consider moving to Flask-Login for scalable auth
🌐 Use Gunicorn or Waitress for deployment
Future Improvements
Google OAuth login
Password reset via email
Monthly budget tracking
Multi-currency support
Export to PDF reports
User profile settings
License

This project is licensed under the MIT License.

<div align="center">

Built with Flask  |  Expense Tracking System | 2026

</div>

---

<div align="center">
  <sub>Built with Flask · 2026 @Python-Project</sub>
</div> -->

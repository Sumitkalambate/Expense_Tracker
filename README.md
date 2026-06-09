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
GET/POST	/login	User logink
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
Werkzeug
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

Built with Flask ❤️ | Secure Expense Tracking System | 2026

</div>
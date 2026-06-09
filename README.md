💸 Expense Tracker Lite
A clean, fast, self-hosted expense tracker built with Flask and SQLite.

Log your daily spending, visualize patterns with live charts, and export data — all in a dark, minimal UI.

📑 Table of Contents
Overview

Features

Tech Stack

Project Structure

Data Model

API Routes

CSV Export Format

Getting Started

Dependencies

Security Notes

License

Overview
Expense Tracker Lite is a single-user, browser-based personal finance tool. It stores every expense in a local SQLite database, requires no external services or cloud accounts, and runs entirely on your machine. The dashboard combines a filterable transaction table with real-time Chart.js visualizations so you can see where your money goes at a glance.

Features
Feature	Details
➕ Add Expenses	Record description, amount (₹), category, and date
🔍 Smart Filtering	Filter the dashboard by date range, category, or both simultaneously
✏️ Inline Editing	Update any field of a saved expense via a dedicated edit form
🗑️ Safe Deletion	Remove individual records with a single POST action
🥧 Pie Chart	Category-wise spending breakdown, filtered in real time
📊 Bar Chart	Day-by-day spending trend across your selected date range
📥 CSV Export	Download your filtered dataset; filename includes the date range automatically
🔔 Flash Notifications	Contextual success and error messages for every action
🌑 Dark UI	Tailwind CSS dark theme (zinc-950 / slate-900) with a brand accent color
Tech Stack
Layer	Technology	Version
Language	Python	3.8+
Web Framework	Flask	3.1.3
ORM	Flask-SQLAlchemy / SQLAlchemy	3.1.1 / 2.0.50
Database	SQLite	(built-in, via Flask)
Templating	Jinja2	3.1.6
Styling	Tailwind CSS	CDN
Charts	Chart.js	CDN
WSGI Toolkit	Werkzeug	3.1.8
Project Structure
Plaintext
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
Note: The instance/ directory and my_database.db are created automatically on first run and are excluded from version control.

Data Model
Python
class Expense(db.Model):
    id          : Integer   (primary key, auto-increment)
    description : String    (max 120 chars, required)
    amount      : Float     (required, must be > 0)
    category    : String    (max 20 chars, required)
    date        : Date      (required, defaults to today)
Supported Categories
Food · Transport · Health · Rent · Utilities

API Routes
Method	Endpoint	Description
GET	/	Dashboard — filterable expense list + charts
POST	/add	Create a new expense record
POST	/delete/<int:id>	Delete an expense by ID
GET	/edit/<int:exp_id>	Render the edit form for an expense
POST	/edit_record/<int:id>	Persist edited expense data
GET	/export_csv	Stream filtered expenses as a downloadable CSV
Filter Query Parameters (on GET /)
Parameter	Type	Description
start	YYYY-MM-DD	Filter expenses on or after this date
end	YYYY-MM-DD	Filter expenses on or before this date
category	string	Limit results to a specific category
CSV Export Format
The export respects the current filter state. The downloaded file is named automatically using the following convention:

Plaintext
Expenses_<start>_to_<end>.csv
Example: Expenses_2026-01-01_to_2026-06-06.csv

Columns Exported: Id, Date (DD-MM-YYYY), Description, Category, Amount

Getting Started
Prerequisites
Python 3.8 or higher

pip

Installation
1. Clone or extract the repository

Bash
git clone <your-repo-url>
cd Expense_Tracker-main
2. Create and activate a virtual environment

Bash
# Create the environment
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
3. Install dependencies

Bash
pip install -r requirements.txt
4. Run the development server

Bash
python app.py
5. Open in your browser
Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

The SQLite database is created automatically at instance/my_database.db on first launch. No migrations or setup commands are required.

Dependencies
Plaintext
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
Security Notes
⚠️ IMPORTANT: These guidelines apply before deploying outside a local machine.

Debug mode: app.run(debug=True) is set in app.py. Disable this in production by setting debug=False or using a production WSGI server such as Gunicorn.

Secret key: The SECRET_KEY is hardcoded. Replace it with a strong, randomly generated value before any non-local deployment:

import secrets
print(secrets.token_hex(32))

*   **Single-user:** There is no authentication layer. Do not expose this application to a public network without adding one.

---

## License

This project is released under the **[MIT License](LICENSE)**.

---

<div align="center">
  <sub>Built with Flask · 2026 @Python-Project</sub>
</div>

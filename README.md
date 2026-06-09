# 💸 Expense Tracker Lite

> A clean, fast, self-hosted expense tracker built with Flask and SQLite.

**Log your daily spending, visualize patterns with live charts, and export data — all in a dark, minimal UI.**

---

## 📑 Table of Contents

- [Overview](#overview)
- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📂 Project Structure](#-project-structure)
- [💾 Data Model](#-data-model)
- [🔌 API Routes](#-api-routes)
- [📊 CSV Export Format](#-csv-export-format)
- [🚀 Getting Started](#-getting-started)
- [📦 Dependencies](#-dependencies)
- [⚠️ Security Notes](#️-security-notes)
- [📜 License](#-license)

---

## Overview

**Expense Tracker Lite** is a single-user, browser-based personal finance tool designed for simplicity and privacy.

✅ **Store every expense** in a local SQLite database  
✅ **No external services** — runs entirely offline  
✅ **Self-hosted** — complete control over your data  
✅ **Minimal UI** — dark theme optimized for easy viewing  

Perfect for tracking personal spending without the bloat of enterprise finance tools.

---

## ✨ Features

| Feature | Details |
|---------|---------|
| ➕ **Add Expenses** | Record description, amount (₹), category, and date |
| 🔍 **Smart Filtering** | Filter by date range, category, or both simultaneously |
| ✏️ **Inline Editing** | Update any field of a saved expense via a dedicated form |
| 🗑️ **Safe Deletion** | Remove individual records with a single action |
| 🥧 **Pie Chart** | Category-wise spending breakdown, filtered in real time |
| 📊 **Bar Chart** | Day-by-day spending trend across your selected date range |
| 📥 **CSV Export** | Download filtered dataset; filename includes date range |
| 🔔 **Flash Notifications** | Contextual success and error messages for every action |
| 🌑 **Dark UI** | Tailwind CSS dark theme with accent colors |

---

## 🛠️ Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Language** | Python | 3.8+ |
| **Web Framework** | Flask | 3.1.3 |
| **ORM** | Flask-SQLAlchemy / SQLAlchemy | 3.1.1 / 2.0.50 |
| **Database** | SQLite | Built-in |
| **Templating** | Jinja2 | 3.1.6 |
| **Styling** | Tailwind CSS | CDN |
| **Charts** | Chart.js | CDN |
| **WSGI Toolkit** | Werkzeug | 3.1.8 |

---

## 📂 Project Structure

```
Expense_Tracker-main/
│
├── app.py                  # Application entry point — routes, models, logic
├── requirements.txt        # Pinned Python dependencies
├── .gitignore              # Excludes instance/, __pycache__, .vscode/
│
└── templates/
    ├── base.html           # Shared layout — header, footer, flash messages
    ├── index.html          # Main dashboard — filters, add form, table, charts
    ├── index1.html         # Alternate dashboard layout
    └── edit.html           # Edit expense form (pre-populated fields)
```

> **Note:** The `instance/` directory and `my_database.db` are created automatically on first run and excluded from version control.

---

## 💾 Data Model

```python
class Expense(db.Model):
    id          : Integer   (primary key, auto-increment)
    description : String    (max 120 chars, required)
    amount      : Float     (required, must be > 0)
    category    : String    (max 20 chars, required)
    date        : Date      (required, defaults to today)
```

### Supported Categories

```
Food  •  Transport  •  Health  •  Rent  •  Utilities
```

---

## 🔌 API Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Dashboard — filterable expense list + charts |
| `POST` | `/add` | Create a new expense record |
| `POST` | `/delete/<int:id>` | Delete an expense by ID |
| `GET` | `/edit/<int:exp_id>` | Render the edit form for an expense |
| `POST` | `/edit_record/<int:id>` | Persist edited expense data |
| `GET` | `/export_csv` | Stream filtered expenses as CSV |

### Filter Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | `YYYY-MM-DD` | Filter expenses on or after this date |
| `end` | `YYYY-MM-DD` | Filter expenses on or before this date |
| `category` | string | Limit results to a specific category |

**Example:**
```
http://127.0.0.1:5000/?start=2026-01-01&end=2026-06-30&category=Food
```

---

## 📊 CSV Export Format

The export respects the current filter state. The downloaded file is named automatically:

```
Expenses_<start>_to_<end>.csv
```

**Example:** `Expenses_2026-01-01_to_2026-06-06.csv`

**Columns Exported:**
```
Id  •  Date (DD-MM-YYYY)  •  Description  •  Category  •  Amount
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.8 or higher
- **pip** (Python package manager)
- **Git** (optional, for cloning)

### Installation

#### 1️⃣ Clone or extract the repository

```bash
git clone <your-repo-url>
cd Expense_Tracker-main
```

#### 2️⃣ Create and activate a virtual environment

```bash
# Create the environment
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

#### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

#### 4️⃣ Run the development server

```bash
python app.py
```

#### 5️⃣ Open in your browser

Navigate to **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your web browser.

> **Note:** The SQLite database is created automatically at `instance/my_database.db` on first launch. No migrations or setup commands required.

---

## 📦 Dependencies

```
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

## ⚠️ Security Notes

**IMPORTANT:** These guidelines apply before deploying outside a local machine.

### 🔴 Debug Mode
```python
app.run(debug=True)  # Currently enabled in app.py
```
**Action:** Disable in production by setting `debug=False` or use a production WSGI server like **Gunicorn**.

### 🔴 Secret Key
The `SECRET_KEY` is hardcoded. **Replace it** with a strong, randomly generated value before any non-local deployment:

```python
import secrets
print(secrets.token_hex(32))
```

### 🔴 Authentication
There is **no authentication layer**. Do not expose this application to a public network without adding authentication.

---

## 📜 License

This project is released under the **[MIT License](LICENSE)**.

---

<div align="center">
  <br>
  <sub>💻 Built with Flask • 2026 @Python-Project</sub>
  <br><br>
  <a href="#-expense-tracker-lite">↑ Back to top ↑</a>
</div>

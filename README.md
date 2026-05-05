# EduPredict AI — Local Deployment Guide

A step-by-step migration and setup guide for deploying the **EduPredict AI Personal Academic Assistant** on a new Windows machine from scratch.

---

## Prerequisites

Before starting, ensure the following software is installed on the new machine:

| Requirement | Version | Download |
|---|---|---|
| **Python** | 3.10 or higher | https://www.python.org/downloads/ |
| **pip** | Included with Python | — |
| **Git** *(optional)* | Any recent version | https://git-scm.com/ |

> **Important:** During Python installation on Windows, make sure to check **"Add Python to PATH"** before clicking Install.

---

## Step 1: Get the Project Files

**Option A — Copy from USB/Drive:**
Copy the entire `ai_student_performance_prediction_system/` folder to your desired location on the new machine (e.g., `C:\Projects\`).

**Option B — Clone from Git:**
```bash
git clone <your-repository-url>
cd ai_student_performance_prediction_system
```

---

## Step 2: Open a Terminal in the Project Folder

1. Open **File Explorer** and navigate to the `ai_student_performance_prediction_system/` folder.
2. Click on the address bar, type `cmd` or `powershell`, and press **Enter**.

Alternatively, open **PowerShell** or **Command Prompt** and navigate manually:
```powershell
cd C:\Projects\ai_student_performance_prediction_system
```

---

## Step 3: Create a Virtual Environment

A virtual environment isolates the project's dependencies from your system Python installation.

```bash
python -m venv venv
```

This creates a `venv/` folder inside your project directory.

---

## Step 4: Activate the Virtual Environment

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

> If PowerShell blocks the script, run this first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

You will know the environment is active when your terminal prompt is prefixed with `(venv)`.

---

## Step 5: Install All Dependencies

With the virtual environment active, install every required library in a single command:

```bash
pip install -r requirements.txt
```

This will install Flask, SQLAlchemy, scikit-learn, pandas, and all other required packages at their correct versions. This step requires an internet connection.

---

## Step 6: Initialize the SQLite Database

> **If you copied the `app/assistant.db` file** from your old machine along with the project, you can **skip this step** — your user accounts and prediction history will be preserved.

If `assistant.db` does **not** exist (fresh machine, fresh start), run the migration script to create all database tables:

```bash
python migrate_db.py
```

Expected output:
```
Dropping existing tables...
Creating new tables...
Database migration complete!
```

---

## Step 7: Train the Machine Learning Model

> **If you copied the `models/` folder** (containing `student_performance_model.pkl` and `scaler.pkl`) from your old machine, you can **skip this step**.

If the `models/` folder is empty or missing, train the model from scratch using the included dataset:

```bash
python train_model.py
```

This will run a GridSearchCV with 5-fold cross-validation. Expected output:
```
Training model with GridSearchCV (5-fold CV)... This may take a few seconds.
Model trained successfully!
Best Parameters: {'max_depth': 8, 'n_estimators': 100}
Model saved at: ...\models\student_performance_model.pkl
Scaler saved at: ...\models\scaler.pkl
Mean Absolute Error: ~2.4
R2 Score: ~0.74
```

---

## Step 8: Run the Flask Development Server

Start the application:

```bash
python run.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

---

## Step 9: Access the Application

Open any web browser and navigate to:

```
http://127.0.0.1:5000
```

You will land on the **EduPredict AI** public landing page. Click **Register** to create a new account, or **Login** if you copied an existing `assistant.db` from your previous machine.

---

## Project Structure Reference

```
ai_student_performance_prediction_system/
│
├── app/
│   ├── __init__.py         # App factory — initializes Flask and SQLAlchemy
│   ├── routes.py           # All URL routes and view logic
│   ├── models.py           # SQLAlchemy database models (User, Task, Note, PredictionHistory)
│   ├── services.py         # Timetable generation and task rollover logic
│   ├── recommender.py      # Rule-based AI recommendation engine
│   ├── templates/          # Jinja2 HTML templates (Tailwind CSS)
│   └── static/             # Static assets (CSS, JS, images)
│
├── data/
│   └── student_data.csv    # Training dataset for the ML model
│
├── models/
│   ├── student_performance_model.pkl   # Trained RandomForest model (generated)
│   └── scaler.pkl                      # StandardScaler (generated)
│
├── migrate_db.py           # Drops and recreates all database tables
├── train_model.py          # Trains and saves the ML model with GridSearchCV
├── run.py                  # Flask application entry point
└── requirements.txt        # Python dependency list
```

---

## Default Login (for migrated databases)

If you transferred the `assistant.db` file, your registered accounts will carry over. If starting fresh, register a new account at `/register`.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Ensure the virtual environment is **activated** (`(venv)` in prompt) before running any command. |
| `Model not found` error | Run `python train_model.py` to generate the `.pkl` files. |
| `Database error` / missing tables | Run `python migrate_db.py` to reset the schema. |
| PowerShell activation blocked | Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` first. |
| Port 5000 already in use | Change the port: `flask run --port 5001` |

---

## Deploying to Render.com (Production)

This section covers deploying EduPredict AI as a live web service on [Render.com](https://render.com) backed by a Neon.tech PostgreSQL database.

### Prerequisites
- A [Render.com](https://render.com) account (free tier works).
- A [Neon.tech](https://neon.tech) account with a database provisioned (free tier works).
- The project pushed to a **GitHub repository** (Render deploys directly from Git).

> **Before pushing to GitHub**, confirm `.env` is listed in `.gitignore` so your secrets are never exposed.

---

### Step 1 — Add Environment Variables in Render

In your Render service dashboard → **Environment** tab, add the following key-value pairs:

| Key | Value |
|---|---|
| `DATABASE_URL` | Your full Neon.tech connection string (copy from Neon dashboard → **Connection string**) |
| `SECRET_KEY` | `e07105b028f78719c82600639728d653e381e5e01aaf276dbf73ea04049005ee` (or generate a new one) |
| `PYTHON_VERSION` | `3.11.0` |

> **Neon connection string format:**
> ```
> postgresql://user:password@ep-xxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
> ```
> Always include `?sslmode=require` — Neon enforces SSL.

---

### Step 2 — Configure the Web Service on Render

When creating a new **Web Service** on Render, fill in the fields exactly as follows:

| Field | Value |
|---|---|
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn run:app --workers 2 --bind 0.0.0.0:$PORT` |

#### Why `run:app`?
Gunicorn needs a `module:variable` reference to locate the Flask app object.
- `run` → refers to `run.py` (the project's entry point file).
- `app` → refers to the `app = create_app()` variable defined inside it.

#### Why `--workers 2`?
Render's free tier has limited RAM. 2 workers is a safe starting point — each worker handles concurrent requests independently.

#### Why `--bind 0.0.0.0:$PORT`?
Render injects the `$PORT` environment variable at runtime. Binding to `0.0.0.0` makes the server reachable from the public internet on that port.

---

### Step 3 — Run Database Migrations on First Deploy

After the first successful deploy, open Render's **Shell** tab for your service and run:

```bash
python migrate_db.py
```

This creates all PostgreSQL tables on Neon. You only need to do this **once** (or after schema changes).

---

### Quick-Reference Cheat Sheet

```
Build Command:  pip install -r requirements.txt
Start Command:  gunicorn run:app --workers 2 --bind 0.0.0.0:$PORT
```

---

*EduPredict AI — Final Year Computer Science Project*
*Lead Developer: Umaima Akmal | Supervisor: Dr. Shahid Fareeed*

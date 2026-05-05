# Deploy EduPredict AI with Neon Postgres

## Recommended Hosting

Use Neon for Postgres and Render for the Flask web app.

Vercel can run Flask apps, but this project uses Flask sessions, SQLAlchemy, scikit-learn, pandas, and generated model files. A normal Python web service is simpler and more reliable for this project than a serverless function bundle.

Netlify is not recommended for this Flask backend.

## 1. Create the Neon Database

1. Create a Neon project.
2. Open **Connect** in the Neon dashboard.
3. Copy the pooled Postgres connection string.
4. Keep `sslmode=require` in the URL.

Example:

```text
postgresql://user:password@ep-example-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require
```

## 2. Deploy on Render

Create a new Render **Web Service** from your GitHub repository.

Use these settings:

```text
Runtime: Python 3
Build Command: pip install -r requirements.txt && python train_model.py
Start Command: gunicorn run:app --workers 2 --bind 0.0.0.0:$PORT
```

Add these environment variables in Render:

```text
DATABASE_URL=<your Neon connection string>
SECRET_KEY=<a strong random secret>
PYTHON_VERSION=3.11.9
```

Generate a secret key locally with:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

## 3. Create Tables in Neon

After the first successful deploy, open the Render shell and run:

```bash
python migrate_db.py
```

This creates missing tables. It does not drop existing data unless you explicitly run with:

```bash
RESET_DATABASE=true python migrate_db.py
```

## 4. Verify

Open:

```text
https://your-app.onrender.com/health
```

Expected response:

```json
{"status":"ok"}
```

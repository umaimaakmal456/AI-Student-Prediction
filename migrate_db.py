import os

from app import create_app, db

app = create_app()
with app.app_context():
    if os.environ.get("RESET_DATABASE", "").lower() == "true":
        print("Dropping existing tables...")
        db.drop_all()

    print("Creating missing tables...")
    db.create_all()
    print("Database migration complete!")

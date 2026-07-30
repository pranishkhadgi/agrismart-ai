import os
import sys

# Set DATABASE_URL before importing app
# Usage:
#   Local SQLite:     python make_admin.py
#   Remote PostgreSQL: DATABASE_URL=your_url python make_admin.py

from app import create_app
from extensions import db
from database.models import User

app = create_app()

with app.app_context():
            db.create_all()

            # Auto-promote admin from environment variable
            admin_email = os.environ.get('ADMIN_EMAIL')
            if admin_email:
                from database.models import User
                user = User.query.filter_by(email=admin_email).first()
                if user and user.role != 'admin':
                    user.role = 'admin'
                    db.session.commit()
                    print(f"Promoted {user.email} to admin.")
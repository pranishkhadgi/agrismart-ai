from app import create_app
from extensions import db
from database.models import User

app = create_app()

with app.app_context():
    email = input("Enter your registered email: ").strip().lower()
    user = User.query.filter_by(email=email).first()
    if user:
        user.role = 'admin'
        db.session.commit()
        print(f"Success! {user.name} is now admin.")
    else:
        print("User not found. Make sure you registered first.")
#Create a admin creation tool by terminal typing
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.config.db import db
from src.models import User
from src.models.users import UserRoleEnum
from src.config.jwt_hash import get_password_hash

def create_admin():
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    confirm_password = input("Confirm admin password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    hashed_password = get_password_hash(password)
    admin_user = User(username=username, email=email, password=hashed_password, role=UserRoleEnum.ADMIN, is_active=True)

    try:
        db.add(admin_user)
        db.commit()
        print(f"Admin user '{username}' created successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error creating admin user: {e}")

if __name__ == "__main__":
    create_admin()
    db.close()
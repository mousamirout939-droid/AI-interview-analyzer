"""
authentication_service.py
============================
Business logic for user registration and login, decoupled from the Flask
route/controller layer so it's independently unit-testable.
"""

from APP.database import db, User
from APP.utils.validators import is_valid_email, is_valid_password, is_valid_name


class AuthError(Exception):
    pass


def register_user(full_name: str, email: str, password: str, confirm_password: str,
                   min_password_length: int = 8) -> User:
    if not is_valid_name(full_name):
        raise AuthError("Please enter your full name (2-150 characters).")
    if not is_valid_email(email):
        raise AuthError("Please enter a valid email address.")
    if password != confirm_password:
        raise AuthError("Passwords do not match.")

    valid, msg = is_valid_password(password, min_length=min_password_length)
    if not valid:
        raise AuthError(msg)

    existing = User.query.filter_by(email=email.lower().strip()).first()
    if existing:
        raise AuthError("An account with this email already exists.")

    user = User(full_name=full_name.strip(), email=email.lower().strip(), role="candidate")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def authenticate_user(email: str, password: str) -> User:
    user = User.query.filter_by(email=(email or "").lower().strip()).first()
    if not user or not user.check_password(password or ""):
        raise AuthError("Invalid email or password.")
    if not user.is_active_account:
        raise AuthError("This account has been deactivated. Contact an administrator.")
    return user

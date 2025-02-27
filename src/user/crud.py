from sqlalchemy.orm import Session
import hashlib
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from models import User

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str, email: str):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    user = User(
        username=username,
        hashed_password=hashed_password,
        email=email,
    )
    
    db.add(user)
    try:
        db.commit()
    except IntegrityError as ex:
        db.rollback()
        return None
    return user

def update_user_profile(db: Session, username: str, first_name: str = None, last_name: str = None, birth_date: str = None, phone_number: str = None):
    user = get_user(db, username)
    if user:
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if birth_date is not None:
            user.birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        if phone_number is not None:
            user.phone_number = phone_number
        
        db.commit()
        return user
    return None

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return user and user.hashed_password == hashed_password

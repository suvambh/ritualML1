from sqlalchemy.orm import Session
from app.database import SessionLocal
from fastapi.templating import Jinja2Templates

# Templates (Jinja2 for HTML rendering)
templates = Jinja2Templates(directory="app/templates")

# Dependency to get a DB session
def get_db():
    db: Session = SessionLocal()   # create a new session
    try:
        yield db                   # let route handlers use it
    finally:
        db.close()                 # close after request finishes

from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import SessionLocal
from app.models import User
import uuid

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---- Dummy User Setup ----
DUMMY_USER_EMAIL = "demo@example.com"

def get_current_user(db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.email == DUMMY_USER_EMAIL).first()
    if not user:
        # Create dummy user
        user = User(
            id=uuid.uuid4(),
            name="Demo User",
            email=DUMMY_USER_EMAIL
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

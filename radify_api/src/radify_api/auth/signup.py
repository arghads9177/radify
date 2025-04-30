from sqlalchemy.orm import Session
from src.radify_api import models, schemas
from .hash import hash_password
from fastapi import HTTPException, status

def create_user(request: schemas.UserCreate, db: Session):
    user_exists = db.query(models.User).filter(models.User.email == request.email).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Another user has already been registered with this email address.")

    hashed_pw = hash_password(request.password)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password_hash=hashed_pw,
        auth_provider=models.AuthProvider.local
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

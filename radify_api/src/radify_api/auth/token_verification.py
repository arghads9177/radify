# src/radify_api/auth/token_verification.py

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from src.radify_api.auth.token import verify_token
from sqlalchemy.orm import Session
from src.radify_api.database import SessionLocal
from src.radify_api.models import User
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/auth/verifyToken")
async def verify_user_token(request: Request, db: Session = Depends(get_db)):
    # Get token from headers (Authorization: Bearer <token>) or query param
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
    else:
        token = request.query_params.get("token")

    if not token:
        raise HTTPException(status_code=400, detail="Token not provided")

    # Verify token
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Extract email from payload
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=400, detail="Email not found in token")

    # Fetch user from DB
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return user info
    return JSONResponse(content={
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": str(user.created_at),  # if applicable
        # Add any other fields you want to expose
    })

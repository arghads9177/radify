# src/radify_api/auth/google_oauth.py

from fastapi import APIRouter, Request, Depends
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from urllib.parse import urlencode
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
import os
from src.radify_api import models, schemas
from src.radify_api.database import SessionLocal
from sqlalchemy.orm import Session

from src.radify_api.auth.token import create_access_token

router = APIRouter()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load from .env
config = Config('.env')
oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)


@router.get("/auth/google")
async def login_via_google(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.get('https://openidconnect.googleapis.com/v1/userinfo', token=token)
    user_info = user_info.json()

    # Check if user already exists
    user = db.query(models.User).filter(models.User.email == user_info["email"]).first()
    if not user:
        new_user = models.User(
            name=user_info.get("name"),
            email=user_info.get("email"),
            password_hash='',
            auth_provider=models.AuthProvider.google
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    
    jwt_token = create_access_token(data={"sub": user_info['email']})

    # Redirect to Angular app with token as query parameter
    params = urlencode({"access-token": jwt_token, "email": user_info['email']})
    redirect_url = f"{os.getenv('WEB_URL')}/auth-callback?{params}"
    return RedirectResponse(url=redirect_url)

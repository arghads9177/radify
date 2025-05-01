# src/radify_api/auth/google_oauth.py

from fastapi import APIRouter, Request, Depends
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from urllib.parse import urlencode
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
import os

from src.radify_api.auth.token import create_access_token

router = APIRouter()

# Load from .env
config = Config('.env')
oauth = OAuth(config)
# oauth.register(
#     name='google',
#     client_id=os.getenv("GOOGLE_CLIENT_ID"),
#     client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     access_token_params=None,
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     api_base_url='https://www.googleapis.com/oauth2/v1/',
#     userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
#     client_kwargs={'scope': 'openid email profile'},
# )
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
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.get('https://openidconnect.googleapis.com/v1/userinfo', token=token)
    user_info = user_info.json()
    
    jwt_token = create_access_token(data={"sub": user_info['email']})

    # Redirect to Angular app with token as query parameter
    params = urlencode({"access-token": jwt_token, "email": user_info['email']})
    redirect_url = f"{os.getenv('WEB_URL')}/auth-callback?{params}"
    return RedirectResponse(url=redirect_url)

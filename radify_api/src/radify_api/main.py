#!/usr/bin/env python
# from radify_api.crew import RadifyApiCrew


# def run():
#     # Replace with your inputs, it will automatically interpolate any tasks and agents information
#     inputs = {
#         'topic': 'AI LLMs'
#     }
#     RadifyApiCrew().crew().kickoff(inputs=inputs)

# app/main.py
from fastapi import FastAPI, Depends, status
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import os
from sqlalchemy.orm import Session
from src.radify_api import models, schemas
from src.radify_api.database import engine, SessionLocal
from .auth import signup, signin, google_oauth
from .utils import rad_generator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="RADify API")

# Add session middleware with a secret key
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")  # Replace with secure key in production
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("WEB_URL")],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],  # or specify ['POST', 'GET', 'OPTIONS']
    allow_headers=["*"],
)
@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "Welcome to the RADify API!"}

app.include_router(signup.router)
app.include_router(signin.router)
app.include_router(google_oauth.router)
app.include_router(rad_generator.router)
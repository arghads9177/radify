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
from sqlalchemy.orm import Session
from src.radify_api import models, schemas
from src.radify_api.database import engine, SessionLocal
from .auth import signup

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="RADify API")

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "Welcome to the RADify API!"}

@app.post("/signup", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return signup.create_user(user, db)

# src/radify_api/utils/rad_generator.py

import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from src.radify_api.database import SessionLocal
from src.radify_api import models
from src.radify_api.agents.rad_creator import generate_rad_text
from src.radify_api.utils.file_handler import extract_text_from_file, save_upload_file

router = APIRouter(prefix="/rad", tags=["RAD Generator"])

UPLOAD_DIR = "uploaded_specs"
GENERATED_DIR = "generated_rads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate")
async def generate_rad(
    job_text: str = Form(...),
    user_id: int = Form(...),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Save uploaded files and insert into work_specifications
        file_texts = []
        work_spec_ids = []

        for file in files:
            file_path = save_upload_file(file, UPLOAD_DIR)
            text = extract_text_from_file(file_path)
            file_texts.append(text)

            work_spec = models.WorkSpecification(
                user_id=user_id,
                filename=file.filename,
                file_url=file_path,
                uploaded_at=datetime.utcnow()
            )
            db.add(work_spec)
            db.commit()
            db.refresh(work_spec)
            work_spec_ids.append(work_spec.id)

        # Combine text
        full_text = job_text + "\n" + "\n".join(file_texts)

        # Generate RAD content
        rad_content = generate_rad_text(full_text)

        # Save RAD to a file
        rad_filename = f"RAD_{uuid.uuid4().hex}.txt"
        rad_path = os.path.join(GENERATED_DIR, rad_filename)
        with open(rad_path, "w") as f:
            f.write(rad_content)

        # Store in rad_documents (linking to latest work_spec_id)
        rad_doc = models.RADDocument(
            user_id=user_id,
            work_spec_id=work_spec_ids[-1],
            filename=rad_filename,
            file_url=rad_path,
            generated_at=datetime.utcnow()
        )
        db.add(rad_doc)
        db.commit()

        return {
            "message": "RAD document generated successfully",
            "rad_content": rad_content,
            "file_url": rad_path,
            "work_spec_ids": work_spec_ids
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

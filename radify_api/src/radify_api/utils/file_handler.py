import os
from typing import Tuple
from fastapi import UploadFile
from uuid import uuid4
from PyPDF2 import PdfReader
import docx2txt

# UPLOAD_DIR = "uploaded_files"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_upload_file(file: UploadFile, UPLOAD_DIR: str) -> Tuple[str, str]:
    """
    Saves the uploaded file and returns (filename, file_path)
    """

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    extension = file.filename.split('.')[-1]
    unique_filename = f"{uuid4()}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return unique_filename, file_path


def extract_text_from_file(file_path: str) -> str:
    """
    Extracts and returns text from a DOCX or PDF file.
    """
    ext = file_path.lower().split('.')[-1]
    text = ""

    if ext == "pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif ext == "docx":
        text = docx2txt.process(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return text.strip()

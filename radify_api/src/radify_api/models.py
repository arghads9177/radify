from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base
import enum

class AuthProvider(enum.Enum):
    local = "local"
    google = "google"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255))
    auth_provider = Column(Enum(AuthProvider), default=AuthProvider.local)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Optional: relationships
    work_specifications = relationship("WorkSpecification", back_populates="user")
    rad_documents = relationship("RADDocument", back_populates="user")

class WorkSpecification(Base):
    __tablename__ = "work_specifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_url = Column(String(512), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="work_specifications")
    rad_documents = relationship("RADDocument", back_populates="work_spec")

class RADDocument(Base):
    __tablename__ = "rad_documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    work_spec_id = Column(Integer, ForeignKey("work_specifications.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_url = Column(String(512), nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="rad_documents")
    work_spec = relationship("WorkSpecification", back_populates="rad_documents")

from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
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

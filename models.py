import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Sponsor(Base):
    __tablename__ = "sponsors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    email = Column(String(200), nullable=False)
    phone = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False, default="prospect")
    notes = Column(Text, nullable=True)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    clients = relationship("Client", back_populates="sponsor", cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        if len(self.password_hash) == 64 and "$" not in self.password_hash:
            if hashlib.sha256(password.encode("utf-8")).hexdigest() == self.password_hash:
                self.set_password(password)
                return True
            return False
        try:
            return pwd_context.verify(password, self.password_hash)
        except Exception:
            return False


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    phone = Column(String(50), nullable=True)
    company = Column(String(200), nullable=True)
    sponsor_id = Column(Integer, ForeignKey("sponsors.id"), nullable=True)
    status = Column(String(50), nullable=False, default="active")
    notes = Column(Text, nullable=True)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sponsor = relationship("Sponsor", back_populates="clients")

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        if len(self.password_hash) == 64 and "$" not in self.password_hash:
            if hashlib.sha256(password.encode("utf-8")).hexdigest() == self.password_hash:
                self.set_password(password)
                return True
            return False
        try:
            return pwd_context.verify(password, self.password_hash)
        except Exception:
            return False

    @property
    def sponsor_name(self):
        return self.sponsor.name if self.sponsor else None


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        if len(self.password_hash) == 64 and "$" not in self.password_hash:
            if hashlib.sha256(password.encode("utf-8")).hexdigest() == self.password_hash:
                self.set_password(password)
                return True
            return False
        try:
            return pwd_context.verify(password, self.password_hash)
        except Exception:
            return False

class ContactMessage(Base):
    __tablename__ = "contact_messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MarketingCampaign(Base):
    __tablename__ = "marketing_campaigns"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    platform = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="planning")
    metrics = Column(Text, nullable=True) # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    referral_code = Column(String, unique=True)
    referred_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    referral_credits = Column(Integer, default=0)  # Reward system
    created_at = Column(DateTime, default=datetime.utcnow)

    referrer = relationship("User", remote_side=[id])

class Referral(Base):
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))
    referred_user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")  # Pending, successful, failed
    date_referred = Column(DateTime, default=datetime.utcnow)

    referrer_user = relationship("User", foreign_keys=[referrer_id], backref="referrals_made")
    referred_user = relationship("User", foreign_keys=[referred_user_id], backref="referrals_received")

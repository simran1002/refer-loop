from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional
import re

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=8, max_length=20)  # Updated password constraint
    referral_code: Optional[str] = None

    @validator("password")
    def validate_password(cls, value):
        """Ensures password contains uppercase, lowercase, digit, and special character"""
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=20)

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: constr(min_length=8, max_length=20)

    @validator("new_password")
    def validate_new_password(cls, value):
        """Reuses password validation for reset"""
        return UserCreate.validate_password(value)

class ReferralResponse(BaseModel):
    referrer_id: int
    referred_user_id: Optional[int] = None
    status: str

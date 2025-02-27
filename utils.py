from passlib.context import CryptContext
import jwt
import os
from datetime import datetime, timedelta
import uuid
from app.config import MAIL_CONFIG
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def generate_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


async def send_email(subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],  
        body=body,
        subtype="html"
    )

    fm = FastMail(MAIL_CONFIG)
    try:
        await fm.send_message(message)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")


def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def generate_referral_code():
    return str(uuid.uuid4())[:8]
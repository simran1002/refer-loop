import os
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig

load_dotenv()

MAIL_PORT = int(os.getenv("MAIL_PORT", "587")) 

MAIL_CONFIG = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,  
    MAIL_SSL_TLS=False,  
)

print("✅ FastAPI Mail configuration loaded successfully!")

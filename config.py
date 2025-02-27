import os
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig

# Load environment variables
load_dotenv()

# Ensure MAIL_PORT is converted properly
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))  # Default to 587 if missing

# ✅ Corrected Email Configuration
MAIL_CONFIG = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,  # Corrected TLS setting
    MAIL_SSL_TLS=False,  # Corrected SSL setting
)

print("✅ FastAPI Mail configuration loaded successfully!")

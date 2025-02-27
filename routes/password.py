from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from app import models, schemas, utils
from app.database import get_db
from app.utils import send_email

router = APIRouter(prefix="/password", tags=["Password Management"])

@router.post("/forgot-password")
async def forgot_password(request: schemas.PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Email not found")

    reset_token = utils.create_access_token({"email": user.email}, expires_delta=timedelta(minutes=15))

    # Send Email with Reset Link
    reset_link = f"https://yourfrontend.com/reset-password?token={reset_token}"
    email_body = f"""
    <h3>Password Reset Request</h3>
    <p>Click the link below to reset your password:</p>
    <a href="{reset_link}">{reset_link}</a>
    <p>If you did not request a password reset, ignore this email.</p>
    """

    # Send the email
    await send_email("Reset Your Password", user.email, email_body)

    return {"message": "Password reset link sent to email", "reset_token": reset_token}

@router.post("/reset-password")
def reset_password(data: schemas.PasswordResetConfirm, db: Session = Depends(get_db)):
    decoded_token = utils.verify_token(data.token)
    if not decoded_token:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.email == decoded_token.get("email")).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    user.password_hash = utils.hash_password(data.new_password)
    db.commit()
    
    return {"message": "Password reset successful"}

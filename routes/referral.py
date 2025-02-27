from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/referral", tags=["Referral System"])

@router.get("/referral-link")
def get_referral_link(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    referral_link = f"https://yourdomain.com/register?referral={user.referral_code}"
    return {"referral_link": referral_link}

@router.get("/referral-stats")
def referral_stats(user_id: int, db: Session = Depends(get_db)):
    referrer = db.query(models.User).filter(models.User.id == user_id).first()
    if not referrer:
        raise HTTPException(status_code=404, detail="User not found")

    successful_referrals = db.query(models.Referral).filter(
        models.Referral.referrer_id == user_id, models.Referral.status == "successful"
    ).count()

    return {"successful_referrals": successful_referrals, "earned_credits": referrer.referral_credits}

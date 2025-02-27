from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request
from starlette.responses import JSONResponse
from datetime import datetime
from app import models, schemas, utils
from app.database import get_db

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
@limiter.limit("5/minute")
def register(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.username == user.username)
    ).first()

    if existing_user:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        if existing_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = utils.hash_password(user.password)
    referral_code = utils.generate_referral_code()

    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        referral_code=referral_code
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # **Handle Referral Logic**
    if user.referral_code:
        referrer = db.query(models.User).filter(models.User.referral_code == user.referral_code).first()
        if referrer:
            referrer.referral_credits += 1  
            db.add(referrer)

            new_referral = models.Referral(
                referrer_id=referrer.id,
                referred_user_id=new_user.id,
                status="successful",
                date_referred=datetime.utcnow()
            )
            db.add(new_referral) 

            db.commit() 

    return {"message": "User registered successfully", "referral_code": referral_code}


@router.post("/login")
@limiter.limit("5/minute") 
def login(request: Request, response: Response, user: schemas.UserLogin, db: Session = Depends(get_db)):  
    user_db = db.query(models.User).filter(models.User.email == user.email).first()
    if not user_db or not utils.verify_password(user.password, user_db.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = utils.create_access_token({"user_id": user_db.id})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,   
        secure=True,      
        samesite="Lax"    
    )

    return {"message": "Login successful and token added successfully in cookie"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}

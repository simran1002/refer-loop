import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app import models, utils


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine) 
    db = TestingSessionLocal()
    yield db  
    db.close()
    Base.metadata.drop_all(bind=engine)  


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def create_test_user(db_session, email="test@example.com", password="password123", referral_code=None):
    hashed_password = utils.hash_password(password)
    user = models.User(email=email, username="testuser", password_hash=hashed_password, referral_code=referral_code)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def get_user_by_email(db_session, email):
    return db_session.query(models.User).filter(models.User.email == email).first()


def test_register_new_user(client):
    response = client.post("/auth/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "referral_code": None
    })
    assert response.status_code == 200
    assert "User registered successfully" in response.json()["message"]

def test_register_existing_user(client, db_session):
    create_test_user(db_session, email="duplicate@example.com")
    response = client.post("/auth/register", json={
        "username": "anotheruser",
        "email": "duplicate@example.com",
        "password": "password123",
        "referral_code": None
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_successful_login(client, db_session):
    create_test_user(db_session, email="loginuser@example.com", password="securepassword")
    response = client.post("/auth/login", json={"email": "loginuser@example.com", "password": "securepassword"})
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful and token added successfully in cookie"

def test_login_invalid_credentials(client, db_session):
    create_test_user(db_session, email="wrongpass@example.com", password="correctpassword")
    response = client.post("/auth/login", json={"email": "wrongpass@example.com", "password": "wrongpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"

def test_register_with_invalid_referral_code(client):
    response = client.post("/auth/register", json={
        "username": "referraluser",
        "email": "referral@example.com",
        "password": "password123",
        "referral_code": "INVALIDCODE"
    })
    assert response.status_code == 400  # Assuming your API handles invalid referral codes properly
    assert response.json()["detail"] == "Invalid referral code"


def test_register_with_self_referral(client, db_session):
    user = create_test_user(db_session, email="selfreferral@example.com")
    response = client.post("/auth/register", json={
        "username": "selfreferraluser",
        "email": "selfreferralnew@example.com",
        "password": "password123",
        "referral_code": user.referral_code  
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "You cannot refer yourself"

def test_successful_referral(client, db_session):
    referrer = create_test_user(db_session, email="referrer@example.com")
    response = client.post("/auth/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "referral_code": referrer.referral_code 
    })
    assert response.status_code == 200
    assert "User registered successfully" in response.json()["message"]


    db_session.refresh(referrer)
    assert referrer.referral_credits == 1


def test_logout(client):
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"

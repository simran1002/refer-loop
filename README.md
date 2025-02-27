# **FastAPI Authentication Test Suite**  

This repository contains a test suite for the authentication system of a FastAPI application. It includes user registration, login, referral-based signups, and logout functionality, tested using `pytest` and `FastAPI TestClient`.  

---

##  Features Covered in Tests
- ✅ **User Registration** (New user, duplicate user, invalid referral code, self-referral, successful referral)  
- ✅ **User Login** (Valid and invalid credentials)  
- ✅ **User Logout**  
- ✅ **Database Setup & Cleanup** (SQLite in-memory database)  

---

## **🛠️ Setup & Installation**  

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/simran1002/refer-loop.git
cd refer-loop

python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```
### **2️⃣ Run Tests**
```bash
pytest test_auth.py -s
```

---

## **📝 API Endpoints**
### Register a new user
**POST** `/auth/register`
### Login and get JWT token
**POST** `/auth/login`
### Logout-Clear the HttpOnly cookie
**POST** `/auth/logout`
### Request password reset
**POST** `/password/forgot-password`
### Reset password using token
**POST** `/password/reset-password`
### Generate referral link for user
**GET** `/referral/referral-link?user_id=1`
### Generate referral statistics
**GET** `/referral/referral-stats?user_id=1`
 
---

## **🐛 Debugging**
Run tests with verbosity for detailed output:
```bash
pytest test_auth.py -v
```
Print API response errors inside tests:
```python
print(response.json())
```

---
![alt text](<Screenshot (551).png>)
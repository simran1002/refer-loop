# **FastAPI Authentication Test Suite**  

This repository contains a test suite for the authentication system of a FastAPI application. It includes user registration, login, referral-based signups, and logout functionality, tested using `pytest` and `FastAPI TestClient`.  

---

## ** Features Covered in Tests**
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

## **📝 Test Cases**

 `test_register_new_user`  Registers a new user 
 `test_register_existing_user`  Prevents duplicate registration 
 `test_register_with_invalid_referral_code`  Rejects invalid referral codes 
 `test_register_with_self_referral`  Blocks self-referral abuse 
 `test_successful_referral`  Validates referral-based registration 
 `test_successful_login`  Logs in with valid credentials 
 `test_login_invalid_credentials`  Rejects invalid login attempts 
 `test_logout`  Ensures successful logout 

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
![alt text](<Screenshot (550).png>)
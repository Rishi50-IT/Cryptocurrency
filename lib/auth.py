import bcrypt
import streamlit as st
from datetime import datetime
from .db import users

def hash_pw(pw: str) -> bytes:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt())

def check_pw(pw: str, hashed: bytes) -> bool:
    try:
        return bcrypt.checkpw(pw.encode(), hashed)
    except Exception:
        return False

def signup(username: str, email: str, password: str) -> tuple[bool, str]:
    username = username.strip().lower()
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    col = users()
    if col.find_one({"username": username}):
        return False, "Username already exists."
    col.insert_one({
        "username": username,
        "email": email.strip(),
        "password": hash_pw(password),
        "created_at": datetime.utcnow(),
    })
    return True, "Account created. Please sign in."

def signin(username: str, password: str) -> tuple[bool, str]:
    username = username.strip().lower()
    user = users().find_one({"username": username})
    if not user or not check_pw(password, user["password"]):
        return False, "Invalid credentials."
    st.session_state["user"] = {"username": user["username"], "email": user.get("email", "")}
    return True, "Welcome back!"

def signout():
    st.session_state.pop("user", None)

def current_user():
    return st.session_state.get("user")

def require_login():
    if not current_user():
        st.warning("Please sign in from the Home page to access this section.")
        st.stop()

import hashlib
import os
import mysql.connector
from dotenv import load_dotenv
from sqlalchemy import create_engine
import streamlit as st

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "dileep8542")
DB_NAME = os.getenv("DB_NAME", "retail_analytics_db")
DB_PORT = os.getenv("DB_PORT", "3306")


# 1. Cached SQLAlchemy Engine (Connection Pool Hang/Freeze ko rokne ke liye)
@st.cache_resource
def get_db_engine():
    """Creates a cached connection pool for fast querying."""
    connection_string = (
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return create_engine(
        connection_string, pool_size=10, max_overflow=20, pool_recycle=3600
    )


# 2. SHA-256 Hashing Helper
def make_hashes(password):
    return hashlib.sha256(str(password).strip().encode("utf-8")).hexdigest()


# 3. MySQL Raw Connection Helper
def get_raw_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        port=int(DB_PORT),
    )


# 4. User Register Function
def register_user(username, password):
    clean_username = username.strip().lower()
    hashed_password = make_hashes(password)
    try:
        conn = get_raw_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (clean_username, hashed_password),
        )
        conn.commit()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print(f"Register Error: {e}")
        return False


# 5. User Login Verification Function
def login_user(username, password):
    clean_username = username.strip().lower()
    hashed_password = make_hashes(password)
    try:
        conn = get_raw_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE LOWER(username) = %s",
            (clean_username,),
        )
        data = cursor.fetchone()
        conn.close()

        if data:
            return data[0] == hashed_password
        return False
    except mysql.connector.Error as e:
        print(f"Login Error: {e}")
        return False
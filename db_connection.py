import os
import mysql.connector
import streamlit as st

def get_db_connection():
    try:
        # Streamlit Cloud par Secrets se connection lega
        if "tidb" in st.secrets:
            connection = mysql.connector.connect(
                host=st.secrets["tidb"]["host"],
                port=int(st.secrets["tidb"]["port"]),
                user=st.secrets["tidb"]["user"],
                password=st.secrets["tidb"]["password"],
                database=st.secrets["tidb"]["database"],
                ssl_verify_identity=False,
                ssl_disabled=False
            )
        else:
            # Local machine par testing ke liye
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="YOUR_LOCAL_MYSQL_PASSWORD",
                database="retail_analytics_db"
            )
        return connection
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None

def init_db():
    """Ensure users table exists in TiDB database"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(50) DEFAULT 'user'
                )
            """)
            conn.commit()
        except Exception as e:
            st.error(f"Table Creation Error: {e}")
        finally:
            cursor.close()
            conn.close()

def login_user(username, password):
    init_db()  # Table exist karti hai ya nahi ye ensure karega
    conn = get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        return user
    except Exception as e:
        st.error(f"Login Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def register_user(username, password, role="user"):
    init_db()  # Table exist karti hai ya nahi ye ensure karega
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, role))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Registration Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
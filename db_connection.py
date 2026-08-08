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
                ssl_verify_identity=True
            )
        else:
            # Local machine par testing ke liye
            connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="YOUR_LOCAL_MYSQL_PASSWORD",  # Apne computer ke MySQL ka password yahan daalein
                database="retail_analytics_db"
            )
        return connection
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None
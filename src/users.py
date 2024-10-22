from db import get_db_connection
import bcrypt
import streamlit as st


# Check if user exists and password is correct
def authenticate_user(username, password):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(
            password.encode("utf-8"), user["password"].encode("utf-8")
        ):
            if user["voted"]:
                st.error("Already Voted")
                return False
            else:
                st.success(f"Welcome {username}")
                return True

        st.error("Invalid username or password")
        return False

    finally:
        connection.close()

import bcrypt
import streamlit as st
from db.voters import get_user_from_db


# Check if user exists and password is correct
def authenticate_user(username, password, connection):
    try:
        user = get_user_from_db(username, connection)

        if user:
            print("User found, checking password")
            password_match = bcrypt.checkpw(
                password.encode("utf-8"), user["password"].encode("utf-8")
            )
            print(f"Password match: {password_match}")

            if password_match:
                if user["voted"]:
                    raise Exception("Already Voted")
                else:
                    st.success(f"Welcome {username}")
                    return user
            else:
                raise Exception("Invalid username or password")

        raise Exception("User not found")

    except Exception as e:
        print(f"Error: {e}")
        st.error(e)
        return None

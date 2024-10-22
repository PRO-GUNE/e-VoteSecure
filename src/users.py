from db import get_db_connection
import bcrypt
import streamlit as st


def get_user_from_db(username):
    cursor = st.session_state.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    return user


def set_voted_in_db(username):
    cursor = st.session_state.connection.cursor()
    cursor.execute("UPDATE users SET voted=1 WHERE username=%s", (username,))
    st.session_state.connection.commit()


@st.cache_data
def get_candidates_from_db():
    cursor = st.session_state.connection.cursor()
    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()
    return candidates


def get_candidate_from_db(candidate):
    cursor = st.session_state.connection.cursor()
    cursor.execute("SELECT * FROM candidates WHERE candidate=%s", (candidate,))
    candidate = cursor.fetchone()
    return candidate


def get_candidate_from_db_by_id(candidate_id):
    cursor = st.session_state.connection.cursor()
    cursor.execute("SELECT * FROM candidates WHERE id=%s", (candidate_id,))
    candidate = cursor.fetchone()
    return candidate


# Check if user exists and password is correct
def authenticate_user(username, password):
    try:
        user = get_user_from_db(username)

        if user:
            print("User found, checking password")
            password_match = bcrypt.checkpw(
                password.encode("utf-8"), user["password"].encode("utf-8")
            )
            print(f"Password match: {password_match}")

            if password_match:
                if user["voted"]:
                    st.error("Already Voted")
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

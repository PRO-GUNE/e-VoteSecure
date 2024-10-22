import streamlit as st
from users import authenticate_user
from db import get_db_connection


# Initialize
if "connection" not in st.session_state:
    st.session_state.connection = get_db_connection()

if "loggedInUser" not in st.session_state:
    st.session_state.loggedInUser = None


# Login section
def login():
    st.subheader("Login Section")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(username, password)

        if user:
            st.session_state.loggedInUser = user


def logout():
    if st.button("Logout"):
        st.session_state.loggedInUser = None


# # Voting section
def vote():
    st.subheader("Voting Section")

    candidates = ["Alice Johnson", "Bob Smith", "Carol Lee", "David Brown", "Eve Davis"]
    candidate = st.selectbox("Candidate", candidates)

    if st.button("Vote"):
        st.success(f"Voted for {candidate}")


# Streamlit app layout
st.title("User Authentication App")

if not st.session_state.loggedInUser:
    login()
else:
    logout()

if st.session_state.loggedInUser:
    vote()

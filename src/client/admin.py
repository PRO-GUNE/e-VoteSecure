# Admin page where admin can request for vote count to start
import streamlit as st
from db.connection import get_db_connection
from config import (
    trusted_authority_get_token_url,
    trusted_authority_vote_submit_url,
    vote_pool_vote_migrate_url,
)
from trustedAuthority.trustedAuthority_votePool import (
    get_vote_pool,
    set_vote_uncounted_in_db,
)
from users import send_otp
from dotenv import load_dotenv
import os
import random
import requests

# Database connection
if "connection" not in st.session_state:
    st.session_state.connection = get_db_connection()

# Admin details
load_dotenv()

ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

if "otp" not in st.session_state:
    st.session_state.otp = None

if "admin" not in st.session_state:
    st.session_state.admin = False

if "token" not in st.session_state:
    st.session_state.token = None


def admin_page():
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Admin Login"):
        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            # Generate OTP
            otp = random.randint(100000, 999999)

            if send_otp(email, otp):
                st.session_state.otp = otp

        else:
            st.error("Invalid credentials")
            return

    if st.session_state.otp:
        entered_otp = st.text_input("Enter OTP")
        if st.button("Verify OTP"):
            if int(entered_otp) == st.session_state.otp:
                token = requests.post(
                    trusted_authority_get_token_url,
                    json={"username": username, "password": password},
                )
                st.session_state.token = token.json()["token"]
                st.session_state.otp = None
                st.session_state.admin = True
                st.success("Admin logged in successfully")


def migrate_votes():
    st.subheader("Migrate Votes")
    if st.button("Migrate Votes"):
        response = requests.post(
            url=vote_pool_vote_migrate_url,  # Ensure the URL is correct
            headers={"Authorization": f"Bearer {st.session_state.token}"},
        )

        if response.status_code == 200:
            st.success("Votes migrated successfully")
        else:
            st.error("Votes migration failed")


def vote_counting():
    st.subheader("Vote Counting")
    st.write("Admin logged in")

    votes = get_vote_pool(st.session_state.connection)

    st.write("Request for Vote counting to start")
    if st.button("Request Vote Counting"):
        response = requests.post(
            trusted_authority_vote_submit_url, json={"votes": votes}
        )

        if response.status_code == 200:
            st.success("Vote counting has started")
        else:
            st.error("Vote counting request failed")

    if st.button("Request Vote Recounting"):
        # Set all counted votes to false
        set_vote_uncounted_in_db(st.session_state.connection)

        response = requests.post(
            trusted_authority_vote_submit_url, json={"votes": votes}
        )

        if response.status_code == 200:
            st.success("Vote counting has started")
        else:
            st.error("Vote counting request failed")


st.title("Admin Page")

if not st.session_state.admin:
    admin_page()
else:
    # Display both vote counting and vote migration buttons separately
    vote_counting()
    st.markdown("---")  # Add a separator line
    migrate_votes()

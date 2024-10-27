# Admin page where admin can request for vote count to start
import streamlit as st
from db.connection import get_db_connection
from db.candidates import get_candidates_from_db
from config import (
    trusted_authority_get_token_url,
    vote_pool_vote_migrate_url,
    trusted_authority_vote_count_url,
)
from trustedAuthority.trustedAuthority_votePool import (
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

if "votes_migrated" not in st.session_state:
    st.session_state.votes_migrated = False

if "results_in" not in st.session_state:
    st.session_state.results_in = False


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
            else:
                st.error("Invalid OTP")


def migrate_votes():
    st.subheader("Migrate Votes")
    if st.button("Migrate Votes"):
        response = requests.post(
            url=vote_pool_vote_migrate_url,
            headers={"Authorization": f"Bearer {st.session_state.token}"},
        )

        if response.status_code == 200:
            st.success("Votes migrated successfully")
            st.session_state.votes_migrated = True
        else:
            st.error("Votes migration failed")


def vote_counting():
    st.session_state.results_in = False
    st.subheader("Vote Counting")
    st.write("Admin logged in")

    st.write("Request for Vote counting")
    if st.button("Request Vote Counting"):
        response = requests.post(
            trusted_authority_vote_count_url,
        )

        if response.status_code == 200:
            st.success("Vote counting has finished")
            st.session_state.results_in = True
        else:
            st.error("Vote counting request failed")


def print_end_result():
    # Display the list of candidates and their votes
    candidates = get_candidates_from_db(st.session_state.connection)
    st.header("Candidates")

    for candidate in candidates:
        st.write(f"{candidate['candidate']} - Vote Count: {candidate['vote_count']}")


st.title("Admin Page")

if not st.session_state.admin:
    admin_page()
else:
    if st.session_state.votes_migrated:
        st.write("Votes have been migrated")
        # Display both vote counting and vote migration buttons separately
        vote_counting()
    else:
        migrate_votes()

    if st.session_state.results_in:
        print_end_result()

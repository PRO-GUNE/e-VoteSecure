import streamlit as st
from db.connection import get_db_connection
from db.voters import set_voted_in_db
from db.candidates import get_candidates_from_db
from client.users import authenticate_user, register_new_user, verify_new_user
from utils.helpers import find_large_prime
from client.crypto import blind_vote, unblind_signature
from client.config import (
    trusted_authority_sign_url,
    trusted_authority_verify_url,
    trusted_authority_vote_count_url,
)
import requests

# Initialize
if "connection" not in st.session_state:
    st.session_state.connection = get_db_connection()

if "loggedInUser" not in st.session_state:
    st.session_state.loggedInUser = None

if "voted" not in st.session_state:
    st.session_state.voted = False

if "candidates" not in st.session_state:
    st.session_state.candidates = get_candidates_from_db(st.session_state.connection)

if "verifyUser" not in st.session_state:
    st.session_state.verifyUser = False


# Login section
def login():
    st.subheader("Login Section")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(username, password, st.session_state.connection)

        if user:
            # Set the loggedInUser session state
            st.session_state.loggedInUser = user

            # Calculate k for user
            st.session_state.k = find_large_prime(32)

    return


# Register user
def register():
    st.subheader("Register Section")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        verify_new_user(username, email, st.session_state.connection)
        st.session_state.verifyUser = True

    if st.session_state.verifyUser:
        # Enter OTP
        entered_otp = st.text_input("Enter OTP")
        if st.button("Verify OTP"):
            if int(entered_otp) == st.session_state.otp:
                register_new_user(username, password, st.session_state.connection)
            else:
                st.error("Invalid OTP")


def logout():
    if st.button("Logout"):
        st.session_state.loggedInUser = None
        st.session_state.voted = False
        st.session_state.k = None
        st.session_state.signed_vote = None
        st.session_state.receipt = None
        st.session_state.verifyUser = False
        st.success("Successfully logged out")
    return


# Voting section
def vote():
    st.subheader("Voting Section")

    candidates = st.session_state.candidates
    candidate_names = [candidate["candidate"] for candidate in candidates]
    candidate = st.selectbox("Candidate", candidate_names)

    if st.button("Vote"):
        # Blind the vote
        m = candidates[candidate_names.index(candidate)]["id"]
        m1 = blind_vote(st.session_state.k, m)

        # Sign the blinded vote -- Done by a trusted authority
        # Send a request to the trusted authority to sign the vote
        payload = {
            "blinded_vote": m1,
            "username": st.session_state.loggedInUser["username"],
        }

        response = requests.post(
            url=trusted_authority_sign_url,
            json=payload,
        )

        # Attempt to parse JSON if status code is OK
        if response.status_code == 200:
            try:
                signed_vote = response.json()["signed_vote"]
                receipt = response.json()["receipt"]
            except ValueError:
                print("Error decoding JSON response")
        else:
            st.error("Error signing the vote")
            return

        st.session_state.signed_vote = signed_vote
        st.session_state.receipt = receipt

        # Submit the unblinded vote to the vote pool
        s = unblind_signature(signed_vote, st.session_state.k)
        # TODO: Submit the vote to the vote pool

        # Update the voted status of the user in the database
        set_voted_in_db(
            st.session_state.loggedInUser["username"], st.session_state.connection
        )
        st.session_state.voted = True
        st.info("Copy the receipt to verify your vote")
        st.code(receipt, language="bash")

        st.success(f"Successfully voted for {candidate}")
        get_vote_count()


# Verify vote
def verify_vote():
    st.subheader("Verify Vote")

    receipt = st.text_input("Receipt")
    if st.button("Verify"):
        payload = {
            "receipt": int(receipt),
            "user_id": st.session_state.loggedInUser["id"],
        }

        response = requests.post(
            url=trusted_authority_verify_url,
            json=payload,
        )

        if response.status_code == 200:
            st.success("Vote verified successfully")
        else:
            st.error("Failed to verify vote")


def get_vote_count():
    response = requests.get(url=trusted_authority_vote_count_url)
    if response.status_code == 200:
        vote_count = response.json()["vote_count"]
        st.session_state.vote_count = vote_count
    return 0


# Streamlit app layout
st.title("User Authentication App")

# Get the vote count from the trusted authority
if "vote_count" not in st.session_state:
    st.session_state.vote_count = get_vote_count()
st.header(f"Vote Count: {st.session_state.vote_count}")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if not st.session_state.loggedInUser:
    if choice == "Login":
        login()
    else:
        register()
else:
    logout()

if st.session_state.loggedInUser:
    if not st.session_state.voted:
        vote()
    else:
        verify_vote()

import streamlit as st
from db.connection import get_db_connection
from db.voters import set_voted_in_db
from db.candidates import (
    get_candidates_from_db,
    get_candidate_from_db_by_id,
)
from client.users import authenticate_user
from utils.helpers import find_large_prime
from client.crypto import blind_vote, unblind_signature, decode_vote
from client.config import trusted_authority_sign_url, trusted_authority_submit_url
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


def logout():
    if st.button("Logout"):
        st.session_state.loggedInUser = None

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

        # Check response status and content
        print(f"Status code: {response.status_code}")
        print(f"Response content: {response.text}")

        # Attempt to parse JSON if status code is OK
        if response.status_code == 200:
            try:
                signed_vote = response.json()["signed_vote"]
                print(signed_vote)
            except ValueError:
                print("Error decoding JSON response")
        else:
            st.error("Error signing the vote")
            return

        st.signed_vote = signed_vote

        # Submit the unblinded vote to the trusted authority
        s = unblind_signature(signed_vote, st.session_state.k)
        response = requests.post(trusted_authority_submit_url, json={"vote": s})

        # Check response status and content
        print(f"Status code: {response.status_code}")
        print(f"Response content: {response.text}")

        # Attempt to parse JSON if status code is OK
        if response.status_code == 200:
            try:
                message = response.json()["message"]
                print(message)
            except ValueError:
                print("Error decoding JSON response")
        else:
            st.error("Error signing the vote")
            return

        # Update the voted status of the user in the database
        set_voted_in_db(
            st.session_state.loggedInUser["username"], st.session_state.connection
        )
        st.session_state.voted = True
        st.success(f"Successfully voted for {candidate}")
        return signed_vote


# Verify vote
def verify_vote():
    st.subheader("Verify Vote")

    if st.button("Verify"):
        m2 = decode_vote(st.signed_vote, st.session_state.k)
        candidate = get_candidate_from_db_by_id(m2, st.session_state.connection)
        st.success(f"You voted for {candidate['candidate']}")


# Streamlit app layout
st.title("User Authentication App")

if not st.session_state.loggedInUser:
    login()
else:
    logout()

if st.session_state.loggedInUser:
    if not st.session_state.voted:
        vote()
    else:
        verify_vote()

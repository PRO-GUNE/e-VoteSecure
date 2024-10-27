import streamlit as st
from db.votepool import add_to_vote_pool
from db.connection import get_db_connection
from db.voters import set_voted_in_db, get_voted_voters_from_db
from db.candidates import get_candidates_from_db
from client.users import (
    authenticate_user,
    register_new_user,
    verify_new_user,
    send_login_email,
)
from utils.helpers import find_large_prime
from client.crypto import blind_vote, unblind_signature
from client.config import (
    trusted_authority_sign_url,
    trusted_authority_verify_url,
    trusted_authority_vote_count_url,
    trusted_authority_get_token_url,
)
import requests

# Initialize
if "connection" not in st.session_state:
    st.session_state.connection = get_db_connection()

if "loggedInUser" not in st.session_state:
    st.session_state.loggedInUser = None

if "token" not in st.session_state:
    st.session_state.token = None

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
            token = requests.post(
                url=trusted_authority_get_token_url,
                json={"username": username},
            )

            if token.status_code == 200:
                # Send login email
                send_login_email(user["email"], username)
                st.success(f"Welcome {username}")
                st.session_state.loggedInUser = user
                st.session_state.token = token.json()["token"]
                st.session_state.k = find_large_prime(32)

            else:
                st.error("Login Failed")

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
                st.rerun()
            else:
                st.error("Invalid OTP")


def logout():
    if st.button("Logout"):
        st.session_state.loggedInUser = None
        st.session_state.token = None
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
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            url=trusted_authority_sign_url,
            json=payload,
        )

        # Attempt to parse JSON if status code is OK
        if response.status_code == 200:
            try:
                signed_vote = response.json()["signed_vote"]

                # Submit the unblinded vote to the vote pool
                vote = unblind_signature(signed_vote, st.session_state.k)
                add_to_vote_pool(vote, st.session_state.connection)
                receipt = response.json()["receipt"]
            except ValueError:
                print("Error decoding JSON response")
        else:
            st.error("Error signing the vote")
            return

        st.session_state.signed_vote = signed_vote
        st.session_state.receipt = receipt

        # Update the voted status of the user in the database
        set_voted_in_db(
            st.session_state.loggedInUser["username"], st.session_state.connection
        )
        st.session_state.voted = True
        st.info("Copy the receipt to verify your vote")
        st.code(receipt, language="bash")

        st.success(f"Successfully voted for {candidate}")
        get_vote_count()
        st.session_state.voted_voters = get_voted_voters_from_db(
            st.session_state.connection
        )


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
            headers={"Authorization": f"Bearer {st.session_state.token}"},
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
    return vote_count


# Streamlit app layout
st.title("e-VoteSecure Voting Platform")

# Get the vote count from the trusted authority
if "vote_count" not in st.session_state:
    st.session_state.vote_count = get_vote_count()
st.header(f"Vote Count: {st.session_state.vote_count}")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)
refrest = st.sidebar.button("Refresh")

if not st.session_state.loggedInUser:
    if choice == "Login":
        login()
    else:
        register()
else:
    if not st.session_state.voted:
        vote()
    else:
        verify_vote()

    logout()

# Display the voted voters
if "voted_voters" not in st.session_state:
    st.session_state.voted_voters = get_voted_voters_from_db(
        st.session_state.connection
    )

voted_voters = {voter["username"] for voter in st.session_state.voted_voters}

if voted_voters:
    st.subheader("Voted Voters")
    st.write(voted_voters)

import streamlit as st
from users import (
    authenticate_user,
    get_candidates_from_db,
    get_candidate_from_db_by_id,
    set_voted_in_db,
)
from db import get_db_connection,add_to_vote_pool
from helpers import find_large_prime
from vote import blind_vote, blind_sign, decode_vote

# Initialize
if "connection" not in st.session_state:
    st.session_state.connection = get_db_connection()

if "loggedInUser" not in st.session_state:
    st.session_state.loggedInUser = None

if "voted" not in st.session_state:
    st.session_state.voted = False

if "candidates" not in st.session_state:
    st.session_state.candidates = get_candidates_from_db()


# Login section
def login():
    st.subheader("Login Section")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(username, password)
        
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
        s1 = blind_sign(m1)
        st.signed_vote = s1
        add_to_vote_pool(s1)

        st.session_state.voted = True
        st.success(f"Voted for {candidate}")

        # Update the voted status of the user in the database
        set_voted_in_db(st.session_state.loggedInUser["username"])
        return s1


# Verify vote
def verify_vote():
    st.subheader("Verify Vote")

    if st.button("Verify"):
        m2 = decode_vote(st.signed_vote, st.session_state.k)
        candidate = get_candidate_from_db_by_id(m2)
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

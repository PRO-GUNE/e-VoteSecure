import streamlit as st
from users import authenticate_user


# Login section
def login():
    st.subheader("Login Section")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            return username


# # Voting section
# def vote(user):
#     st.subheader("Voting Section")

#     candidates = ["Alice Johnson", "Bob Smith", "Carol Lee", "David Brown", "Eve Davis"]
#     candidate = st.select_slider("Candidate", candidates)

#     if st.button("Vote"):
#         if submit_vote(candidate, user):
#             st.success()


# Streamlit app layout
st.title("User Authentication App")

login()

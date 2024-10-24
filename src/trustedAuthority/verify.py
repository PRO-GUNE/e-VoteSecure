import streamlit as st
from db.connection import get_db_connection
from db.voters import get_user_from_id_from_db
from db.candidates import get_candidates_from_db
from crypto import decrypt_receipt

connection = get_db_connection()

st.title("e-VoteSecure Verify Token")

# Get the receipt
receipt = st.text_input("Receipt")

if st.button("Verify"):
    # Decode the receipt
    user_id = decrypt_receipt(receipt)

    # Check if the user is in the database
    user = get_user_from_id_from_db(user_id, connection)
    if user:
        st.success("Vote Verified Successfully")
    else:
        st.error("Verification Failed")

# Display the list of candidates and their votes
candidates = get_candidates_from_db(connection)
st.header("Candidates")

for candidate in candidates:
    st.write(f"{candidate['candidate']} - Vote Count: {candidate['vote_count']}")

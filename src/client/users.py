import bcrypt
import streamlit as st
from db.voters import get_user_from_db, set_user_in_db

import random
import smtplib
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

# Email settings from environment variables
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# Send OTP via email
def send_otp(email, otp):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = email
        msg["Subject"] = "Your OTP for Registration"

        body = f"Your OTP for registration is {otp}. Please enter it to complete your registration."
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, email, msg.as_string())
        server.quit()

        st.success("OTP sent successfully")
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False


# Send Login email
def send_login_email(email, username):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = email
        msg["Subject"] = "Login Activity"

        body = f"You just logged in to the voting system as {username}."
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, email, msg.as_string())
        server.quit()

        st.success("Login email sent successfully")

    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False


# Check if user exists and password is correct
def authenticate_user(username, password, connection):
    try:
        user = get_user_from_db(username, connection)

        if user:
            print("User found, checking password")
            password_match = bcrypt.checkpw(
                password.encode("utf-8"), user["password"].encode("utf-8")
            )
            print(f"Password match: {password_match}")

            if password_match:
                if user["voted"]:
                    raise Exception("Already Voted")
                else:
                    return user
            else:
                raise Exception("Invalid username or password")

        raise Exception("User not found")

    except Exception as e:
        print(f"Error: {e}")
        st.error(e)
        return None


def register_new_user(username, password, connection):
    try:
        # Hash password
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Insert user into database
        set_user_in_db(username, hashed_password, connection)
        st.success("User registered successfully")
        st.session_state.verifyUser = False

    except Exception as e:
        st.error(f"Failed to verify OTP: {e}")
        return False


def verify_new_user(username, email, connection):
    try:
        # Check if user already exists
        user = get_user_from_db(username, connection)
        if user:
            raise Exception("User already exists")

        # Generate OTP
        otp = random.randint(100000, 999999)

        if send_otp(email, otp):
            st.session_state.otp = otp
            return True

    except Exception as e:
        st.error(f"Failed to register user: {e}")
        return False

import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="🏠 Mortgage Assistant", page_icon="🏠")

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.password = ""
    st.session_state.real_name = ""
    st.session_state.in_chat = False

# -------------------------------
# Login Page
# -------------------------------
if not st.session_state.logged_in:
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            test_login = requests.get(
                f"{BACKEND_URL}/me",  # dummy call to check auth
                auth=HTTPBasicAuth(username, password)
            )
            if test_login.status_code == 200:
                user_info = test_login.json()
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.password = password
                st.session_state.real_name = user_info["name"]
                st.success("Logged in successfully!")
            else:
                st.error("Login failed. Check credentials.")

        except Exception as e:
            st.error(f"Error:{e}")


elif not st.session_state.in_chat:
    st.title(f"🏠 Welcome, {st.session_state.real_name}!")
    st.write("Click below to start the mortgage eligibility check")

    if st.button("🧮 Launch Mortgage Checker"):
        st.session_state.in_chat = True

    if st.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.password = ""
        st.session_state.real_name = ""
        st.session_state.in_chat = False

# -------------------------------
# Chat Page (Simple Form UI)
# -------------------------------
elif st.session_state.in_chat:
    st.title("💬 Mortgage Eligibility Bot")
    st.write("Ask about your or someone else's eligibility")

    choice = st.radio(
        "Whose eligibility do you want to check?",
        ["Mine", "Someone else"]
    )

    customer_id = ""
    if choice == "Someone else":
        customer_id = st.text_input("Enter their customer ID")

    user_query = st.text_area("Your Question")

    if st.button("Check Eligibility"):
        try:
            # Prepare query params only if customer_id is given
            params = {"customer_id": customer_id.strip()} if customer_id else {}

            # Make POST request to /assess endpoint
            response = requests.post(
                f"{BACKEND_URL}/assess",
                params=params,
                auth=HTTPBasicAuth(st.session_state.username, st.session_state.password)
            )

            # Catch HTTP errors explicitly
            result = response.json()

            # ✨ Add this block to handle different response formats ✨
            if isinstance(result['answer'], dict) and 'text' in result['answer']:
                # Handle the dictionary format with 'text' key
                display_text = result['answer']['text']
            else:
                # Handle the normal string response
                display_text = result['answer']

            st.markdown(f"### ✅ Response\n{display_text}")
            st.success("Scroll up for the result ⬆️")

        except requests.exceptions.HTTPError:
            try:
                # If API returned an error JSON with 'detail'
                error_detail = response.json().get("detail", "Something went wrong.")
                st.error(f"❌ Error: {error_detail}")
            except ValueError:
                # Response is not valid JSON
                st.error("❌ Error: Server returned a non-JSON response.")
        except Exception as e:
            st.error(f"⚠️ Unexpected error: {e}")

    if st.button("❌ End Chat"):
        st.session_state.in_chat = False

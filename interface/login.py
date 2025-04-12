import streamlit as st

# Simple username/password map for demo (replace with secure method later)
USER_CREDENTIALS = {
    "vish": "password123",
    "demo": "demo"
}

def login():
    st.title("🔐 GenAssist Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username} 👋")
            st.rerun()
        else:
            st.error("Invalid username or password")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

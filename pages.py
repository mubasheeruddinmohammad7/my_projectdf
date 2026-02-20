import streamlit as st

def show_profile():
    st.subheader("Profile")

    username = st.text_input("Enter your name", st.session_state.username)

    if st.button("Save"):
        st.session_state.username = username
        st.success("Profile updated!")
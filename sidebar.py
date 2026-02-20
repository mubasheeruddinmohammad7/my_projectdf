import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("Navigation")

        pages = [
            "Home", "Marketplace", "AR Studio",
            "Sustainability", "2D to 3D",
            "Profile", "Wishlist", "Analytics", "Settings"
        ]

        for page in pages:
            if st.button(page):
                st.session_state.current_page = page
                st.rerun()
import streamlit as st

def init_session():
    if 'user' not in st.session_state:
        st.session_state.user = {
            'name': 'Demo User',
            'email': 'demo@digitalfashion.com',
            'wallet': '0x1234...5678',
            'member_since': '2024-01-15',
            'currency': 'INR'
        }

    if 'cart' not in st.session_state:
        st.session_state.cart = []

    if 'impact' not in st.session_state:
        st.session_state.impact = {
            'items': 0,
            'water_saved': 0,
            'co2_saved': 0,
            'level': 1,
            'points': 250
        }

    if 'nfts' not in st.session_state:
        st.session_state.nfts = []

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

    if 'wishlist' not in st.session_state:
        st.session_state.wishlist = []
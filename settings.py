import streamlit as st

def show_settings():
    st.subheader("Settings")

    if st.button("Clear Cart"):
        st.session_state.cart = []
        st.success("Cart cleared!")

    if st.button("Reset Wishlist"):
        st.session_state.wishlist = []
        st.success("Wishlist cleared!")
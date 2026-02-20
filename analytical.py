import streamlit as st

def show_analytics():
    st.subheader("Analytics")

    st.write(f"Items in Cart: {len(st.session_state.cart)}")
    st.write(f"Wishlist Items: {len(st.session_state.wishlist)}")
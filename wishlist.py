import streamlit as st

def show_wishlist():
    st.subheader("Wishlist")

    if not st.session_state.wishlist:
        st.write("Wishlist is empty.")
    else:
        for item in st.session_state.wishlist:
            st.write(item["name"])
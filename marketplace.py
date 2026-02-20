import streamlit as st
from data.products import PRODUCTS
from utils.helper import format_price
from utils.nft import mint_nft

def show_marketplace():
    st.subheader("Marketplace")

    for product in PRODUCTS:
        st.write(f"### {product['name']}")
        st.write(f"Price: {format_price(product['price'])}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Add to Cart {product['id']}"):
                st.session_state.cart.append(product)
                st.success("Added to cart!")

        with col2:
            if st.button(f"Mint NFT {product['id']}"):
                message = mint_nft(product["name"], st.session_state.username)
                st.info(message)

    st.divider()
    st.subheader("Cart")

    if not st.session_state.cart:
        st.write("Cart is empty.")
    else:
        total = 0
        for item in st.session_state.cart:
            st.write(item["name"])
            total += item["price"]

        st.write(f"Total: {format_price(total)}")
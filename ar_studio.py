import streamlit as st
from utils.image_processing import process_image

def show_ar_studio():
    st.subheader("AR Studio")

    uploaded_file = st.file_uploader("Upload your photo", type=["jpg", "png"])

    if uploaded_file:
        image = process_image(uploaded_file)
        st.image(image, caption="Preview", use_column_width=True)
        st.success("Virtual try-on preview loaded.")
import streamlit as st
from config import init_session
from components.sidebar import render_sidebar
from components.header import render_header
from components.footer import render_footer

from pages.home import show_home
from pages.marketplace import show_marketplace
from pages.ar_studio import show_ar_studio
from pages.sustainability import show_sustainability
from pages.profile import show_profile
from pages.wishlist import show_wishlist
from pages.analytical import show_analytics
from pages.settings import show_settings
from pages.converter_2d3d import show_converter

st.set_page_config(page_title="Digital Fashion", layout="wide")

init_session()
render_sidebar()
render_header()

page = st.session_state.current_page

if page == "Home":
    show_home()
elif page == "Marketplace":
    show_marketplace()
elif page == "AR Studio":
    show_ar_studio()
elif page == "Sustainability":
    show_sustainability()
elif page == "2D to 3D":
    show_converter()
elif page == "Profile":
    show_profile()
elif page == "Wishlist":
    show_wishlist()
elif page == "Analytics":
    show_analytics()
elif page == "Settings":
    show_settings()

render_footer()
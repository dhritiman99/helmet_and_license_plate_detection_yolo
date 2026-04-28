import streamlit as st
import os 
from views.login import login
from db import init_db


init_db()
if "logged_user" not in st.session_state:
    st.session_state.logged_user = None

login = st.Page(
    page="views/login.py",
    title="Log In"    
)
home = st.Page(
    page="views/home.py",
    title="Home",
    default=True
)
violations = st.Page(
    page="views/violations.py",
    title="Violations"
)

nav_pages = [login,home, violations]


st.logo('static/logo.png', size="large")
st.sidebar.text('Helmet, License Plate Detection')
if st.sidebar.button("Log Out"):
    st.session_state.logged_user = None
    st.switch_page("views/home.py") 
page = st.navigation(pages=nav_pages,position="sidebar")
page.run()

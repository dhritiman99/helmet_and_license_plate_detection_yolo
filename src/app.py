import streamlit as st
import os 
from views.login import login
from db import init_db


init_db()
if "logged_user" not in st.session_state:
    st.session_state.logged_user = None

home = st.Page(
    page="views/home.py",
    title="Home",
    default=True
)
violations = st.Page(
    page="views/violations.py",
    title="Violations"
)

if not st.session_state.logged_user:
    login()
else:
    st.logo('static/logo.jpg')
    st.sidebar.text('Helmet, License Plate Detection')
    page = st.navigation(pages=[home, violations])
    page.run()

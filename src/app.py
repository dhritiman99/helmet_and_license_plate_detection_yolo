import streamlit as st
import os 
from db import init_db


init_db()

home = st.Page(
    page="views/home.py",
    title="Home",
    default=True
)
violations = st.Page(
    page="views/violations.py",
    title="Violations"
)

nav_pages = [home, violations]


st.logo('static/logo.png', size="large")
st.sidebar.text('Helmet, License Plate Detection')
page = st.navigation(pages=nav_pages,position="sidebar")
page.run()

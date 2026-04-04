import streamlit as st
import os 


home = st.Page(
    page="views/home.py",
    title="Home",
    default=True
)
violations = st.Page(
    page="views/violations.py",
    title="Violations"
)

st.logo('static/logo.jpg')
st.sidebar.text('created by d7n')

page = st.navigation(pages=[home, violations])
page.run()

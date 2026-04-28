import streamlit as st
from components.detector import detector

if st.session_state.logged_user is None:
    st.switch_page('views/login.py')
else:
    st.title("Detect Riders without Helmets")
    detector()
import streamlit as st
from db.schemas.user import add_user,login_user


def login():
    login = st.container()
    with login:
        add_user(
            name = "admin",
            email = "admin@admin.com",
            password = "admin"
        )
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password")
        status_txt = st.empty()
        login_btn = st.button(
            "Log In"
        )



        if login_btn:
            login = st.spinner()
            st.session_state.logged_user = login_user(username,password)
            if st.session_state.logged_user is None:
                status_txt.text("Invalid Username or Password")
            else:
                st.rerun()
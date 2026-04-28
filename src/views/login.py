import streamlit as st
from db.schemas.user import add_user,login_user
from streamlit_redirect import redirect

def login():
    if st.session_state.logged_user is not None:
        st.switch_page('views/home.py')
    
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
    """, unsafe_allow_html=True)
    login = st.container()
    with login:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password")
        status_txt = st.empty()
        login_btn = st.button(
            "Log In"
        )

        if login_btn:
            login = st.spinner()
            logged_user = login_user(username,password)
            if logged_user is None:
                status_txt.text("Invalid Username or Password")
            else:
                st.session_state.logged_user = logged_user
                st.switch_page('views/home.py')


    
login()
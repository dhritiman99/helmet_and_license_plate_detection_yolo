
import streamlit as st 
from utils.image import buffer_to_img

def show_violations(violations: list):
    st.title('Detected Violations')

    for violation in violations:
        with st.container(height=300):
            c1, c2 = st.columns(2)
            with c1:
                st.image(buffer_to_img(violation['rider_img']), channels="BGR", use_container_width=True)
            with c2:
                st.image(buffer_to_img(violation['plate_img']), channels="BGR", )
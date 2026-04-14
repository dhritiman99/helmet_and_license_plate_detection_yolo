
import streamlit as st 
from utils.image import buffer_to_img

def show_violations(violations: dict, img_channel="BGR"):

    st.title('Detected Violations')
    for violation_id in violations:
        with st.container(height=300):
            c1, c2 = st.columns(2)
            with c1:
                st.image(buffer_to_img(violations[violation_id]['rider_img']), channels=img_channel, width='stretch')
            with c2:
                st.image(buffer_to_img(violations[violation_id]['plate_img']), channels=img_channel, width=500)

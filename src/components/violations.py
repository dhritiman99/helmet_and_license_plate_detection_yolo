
import streamlit as st 
from utils.image import buffer_to_img, img_np_to_bytes
from db.schemas.violation import add_violation


def show_violations(violations: dict, img_channel="BGR"):

    st.title('Detected Violations')
    for violation_id in violations:
        add_violation(
            rider_img=img_np_to_bytes(violations[violation_id]['rider_img']),
            plate_img=img_np_to_bytes(violations[violation_id]['plate_img']),
            plate_txt=violations[violation_id]['plate_txt']
        )
        with st.container(height=300):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.image(buffer_to_img(violations[violation_id]['rider_img']), channels=img_channel, width='stretch')
            with c2:
                st.image(buffer_to_img(violations[violation_id]['plate_img']), channels=img_channel, width=500)
            with c3:
                if "plate_txt" in violations[violation_id]:
                    if not violations[violation_id]['plate_txt'] == "":
                        st.text(f"Plate : {violations[violation_id]['plate_txt']}")

import streamlit as st
from db.schemas.violation import get_violations, del_violation

st.text("Violations")
violations = get_violations()


for violation in violations:
    with st.container(
        height=200,
        horizontal=True,
        horizontal_alignment="center"
    ):
        st.image(violation.rider_img, width=200)
        st.image(violation.plate_img, width=100)
        st.text(violation.plate_txt)
        if st.button("Delete",key=violation.id):
            del_violation(violation.id)
            st.rerun()

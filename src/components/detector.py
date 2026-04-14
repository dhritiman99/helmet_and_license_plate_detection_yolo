import streamlit as st

from .video import process_video

from .image import process_image

def detector():


    upload = st.file_uploader(

        "upload image / video",
        type=['jpg','png','webp','mp4']

    )

    if upload is not None:
        ftype = upload.type
        if "image" in ftype:
            process_image(upload)
        elif "video" in ftype:
            process_video(upload)
    
    

    
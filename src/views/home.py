import streamlit as st
from components.detector import detector


st.title("Detect Riders without Helmets")
detector()
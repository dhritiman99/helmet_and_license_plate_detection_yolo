import streamlit as st
from ultralytics import YOLO
import os

@st.cache_resource
def load_models():
    model = YOLO('weights/best.pt')
    return model
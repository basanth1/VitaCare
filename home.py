import streamlit as st
from components.homepage_sections import (
    render_hero,
    render_about,
    render_services,
    render_doctors,
    render_contact,
)
from pathlib import Path

st.set_page_config(layout="wide")

# Load CSS
def load_css():
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
st.markdown("""
    <style>
     header[data-testid="stHeader"] {
            display: none;
        }
        footer {
            visibility: hidden;
        }
        .block-container {
            padding: 0 3rem;
            background-color: #f4f1fa;
        }

        section.main > div {
            background-color: #f4f1fa;
        }

        /* Sidebar */
        .css-1d391kg {  /* This class may vary with Streamlit versions */
            background-color: #e9c6ef !important;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-thumb {
            background: #8032a8;
            border-radius: 10px;
        }

        /* Fix buttons on mobile */
        button {
            font-size: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
# --- Page Sections ---
render_hero()
render_about()
render_services()
render_doctors()
render_contact()

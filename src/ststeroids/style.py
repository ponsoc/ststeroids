import streamlit as st


class Style:
    def __init__(self, style_file: str):

        self.style_file = style_file

    def apply_style(self):
        with open(self.style_file) as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

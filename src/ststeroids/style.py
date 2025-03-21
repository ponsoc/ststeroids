import streamlit as st


# pylint: disable=too-few-public-methods
class Style:
    """
    A class for applying custom CSS styles to a Streamlit app.
    """

    def __init__(self, style_file: str):
        """
        Initializes the Style class with the specified CSS file.

        :param style_file: The path to the CSS file containing the styles.
        """
        self.style_file = style_file

    def apply_style(self):
        """
        Reads the CSS file and applies its styles to the Streamlit app.

        :return: None
        """
        with open(self.style_file) as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

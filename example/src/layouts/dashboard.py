import streamlit as st
from shared import ComponentIDs
from ststeroids import Flow, Layout


class DashboardLayout(Layout):
    def __init__(self):
        st.empty()
        

    def render(self):
        st.write("Nog niet ingelogd. Gebruik het menu of ververs de pagina.")
        

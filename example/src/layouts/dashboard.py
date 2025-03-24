import streamlit as st
from components import MetricComponent
from shared import ComponentIDs
from ststeroids import Layout


class DashboardLayout(Layout):
    def __init__(self):
       self.total_movies = MetricComponent(ComponentIDs.total_movies,"Total movies")
       self.avg_rating = MetricComponent(ComponentIDs.avg_rating, "Avg. Rating")
        

    def render(self):
        left, right = st.columns([1,1])
        with left:
            self.total_movies.render()
        with right:
            self.avg_rating.render()


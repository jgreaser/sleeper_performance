import streamlit as st
import plotly.express as px

def display_player_stats(player_name: str, weekly_points: list):
    fig = px.line(
        x=list(range(1, len(weekly_points) + 1)),
        y=weekly_points,
        labels={'x': 'Week', 'y': 'PPR Points'},
        title=f"{player_name}'s Performance"
    )
    st.plotly_chart(fig)

import plotly.express as px
import streamlit as st
import pandas as pd

def display_performance_chart(filtered_df, username):
    """Display single user performance chart"""
    fig = px.line(
        filtered_df, 
        x='Season',
        y='Games Above 500',
        title=f"Performance Over Time - {username}",
        markers=True
    )
    
    # Add standings annotations
    for _, row in filtered_df.iterrows():
        fig.add_annotation(
            x=row['Season'],
            y=row['Games Above 500'],
            text=f"#{row['Standing']}/{row['Total Teams']}",
            showarrow=False,
            yshift=20
        )
        
    return st.plotly_chart(fig, use_container_width=True)

def display_comparison_chart(filtered_df, compare_filtered, username, selected_manager_name):
    """Display comparison chart between two users"""
    compare_fig = px.line(
        pd.concat([
            filtered_df.assign(Manager=username),
            compare_filtered.assign(Manager=selected_manager_name)
        ]),
        x='Season',
        y='Games Above 500',
        color='Manager',
        title="Performance Comparison",
        markers=True
    )
    
    # Add standings annotations for both users
    for _, row in filtered_df.iterrows():
        compare_fig.add_annotation(
            x=row['Season'],
            y=row['Games Above 500'],
            text=f"#{row['Standing']}/{row['Total Teams']}",
            showarrow=False,
            yshift=20
        )
    
    for _, row in compare_filtered.iterrows():
        compare_fig.add_annotation(
            x=row['Season'],
            y=row['Games Above 500'],
            text=f"#{row['Standing']}/{row['Total Teams']}",
            showarrow=False,
            yshift=20
        )
        
    return st.plotly_chart(compare_fig, use_container_width=True)
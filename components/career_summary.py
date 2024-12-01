import streamlit as st


def format_stat(count, total):
    """Format a stat with its percentage of total"""
    if total == 0:
        return "0 (0%)"
    percentage = (count / total) * 100
    return f"{count} ({percentage:.0f}%)"

def display_career_summary(filtered_df):
    """Display career summary statistics"""
    st.subheader("Career Summary")
    total_seasons = filtered_df['Season'].nunique()
    
    # Championships section
    championship_col1, championship_col2 = st.columns([1, 4])

    with championship_col1:
        championships = filtered_df['Is Champion'].sum()  # Get actual championship count
        st.metric(
            "Championships 👑",
            format_stat(championships, total_seasons),
            help="League Championships won"
        )

    # Add separator
    st.markdown("---")

    # Regular career stats in 5-column layout
    stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5)

    with stat_col1:
        reg_season_wins = filtered_df['Is Regular Season Winner'].sum()
        st.metric(
            "Regular Season Wins 🏆",
            format_stat(reg_season_wins, total_seasons)
        )

    with stat_col2:
        top_6 = filtered_df['In Top 6'].sum()
        st.metric(
            "Top 6 Finishes 📈",
            format_stat(top_6, total_seasons)
        )

    with stat_col3:
        bottom_4 = filtered_df['In Bottom 4'].sum()
        st.metric(
            "Bottom 4 Finishes 📉",
            format_stat(bottom_4, total_seasons)
        )

    with stat_col4:
        avg_standing = filtered_df['Standing'].mean()
        st.metric(
            "Average Standing",
            f"{avg_standing:.1f}"
        )

    with stat_col5:
        win_pct = filtered_df['Games Above 500'].mean()
        st.metric(
            "Avg Games +/-",
            f"{win_pct:.1f}"
        )
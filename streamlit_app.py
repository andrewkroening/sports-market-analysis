import streamlit as st
import pandas as pd
import altair as alt
import folium

# read the four datasets
league_df = pd.read_csv("data/league_data.csv")
team_df = pd.read_csv("data/team_data.csv")
social_df = pd.read_csv("data/social_data.csv")
team_df = pd.read_csv("data/team_data.csv")


# create four tabs
tabs = ["League Info", "Team Info", "Social Media Data", "Team Locations"]

tab1, tab2, tab3, tab4 = st.tabs(tabs)

with tab1:
    
    # make an altair chart of the season and playoff dates
    st.write("Season and Playoff Dates")

    # create a chart
    chart = alt.Chart(league_df).mark_bar().encode(
        x='season',
        y='playoff_start'
    ).properties(
        width=600,
        height=400
    )
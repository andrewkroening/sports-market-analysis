import streamlit as st
import pandas as pd
import folium
import matplotlib as mpl
import matplotlib.pyplot as plt


########## Need to move this later to a separate file ##########
def unnormalize(x):
    """Function to unnormalize values

    Args:
        x: float

    Returns:
        hexcolor: color in hex format
    """

    # make an colormap for the nodes
    plot_cmap = plt.cm.RdYlGn

    # define ranges
    OldMin = 15.458358298382265
    OldMax = 130.55555555555554
    NewMin = 10
    NewMax = 255

    # define the old value
    OldValue = x

    # calculate the new value
    OldRange = OldMax - OldMin
    NewRange = NewMax - NewMin
    new_color = int((((OldValue - OldMin) * NewRange) / OldRange) + NewMin)

    # get the color from the colormap
    new_color = plot_cmap(new_color)

    # convert the node color to hex
    hexcolor = mpl.colors.rgb2hex(new_color)

    return hexcolor


def get_size(x):
    """Function to unnormalize values

    Args:
        x: float

    Returns:
        new_size: color in hex format
    """

    # define ranges
    OldMin = 2480000
    OldMax = 36750000
    NewMin = 5
    NewMax = 50

    # define the old value
    OldValue = x

    # calculate the new value
    OldRange = OldMax - OldMin
    NewRange = NewMax - NewMin
    new_size = int((((OldValue - OldMin) * NewRange) / OldRange) + NewMin)

    return new_size


########## Need to move this later to a separate file ##########

# read the datasets
league_df = pd.read_csv("data/league_data.csv", parse_dates=True)
team_df = pd.read_csv("data/team_data.csv", parse_dates=True)

# Set a page title and an icon
st.set_page_config(page_title="Sports Market Analysis Dashboard", page_icon="🏟️")

# Add a title
st.title("Sports Market Analysis Dashboard")

# add a subtitle
st.write(
    "The circle size is the total number of followers for each team. The color of the circle is the revenue per follower."
)

# Add a selectbox to the sidebar:
st.sidebar.title("Select a league")
league = st.sidebar.selectbox("Choose a league", league_df["League"].unique())


# create a map
m = folium.Map(
    location=[39.8283, -98.5795],
    tiles="CartoDB positron",
    zoom_start=4,
    min_lat=20,
    max_lat=50,
    min_lon=-130,
    max_lon=-60,
    max_bounds=True,
    max_zoom=6,
    min_zoom=4,
)

# add markers to the map
for i in range(len(team_df)):

    cir_size = get_size(team_df.iloc[i]["TotalFollowers"])
    cir_fill = unnormalize(team_df.iloc[i]["RevPerFollower"])

    folium.CircleMarker(
        location=[
            team_df.iloc[i]["TeamLocationLat"],
            team_df.iloc[i]["TeamLocationLong"],
        ],
        radius=cir_size,
        color="black",
        fill=True,
        fill_color=cir_fill,
        fill_opacity=0.7,
        tooltip=f"{team_df.iloc[i]['TeamName']}<br>Revenue per Follower: ${team_df.iloc[i]['RevPerFollower']:,.2f}<br>Total Followers: {team_df.iloc[i]['TotalFollowers']:,.0f}",
    ).add_to(m)

st.write(m)

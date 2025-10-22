################################################ CITI BIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from PIL import Image


########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title='Citi Bikes Strategy Dashboard', layout='wide')
st.title("Citi Bikes: Strategy Dashboard")

# Define side bar
st.sidebar.title("Anaysis Menu")
page = st.sidebar.selectbox('Choose a section of the analysis',
    ["Intro page", "Weather and bike usage",
     "Most popular stations",
     "Interactive Map with aggregated Trip Data", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('trips_weather.csv')
top20 = pd.read_csv('top20_station.csv', index_col = 0)
def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

df['date'] = pd.to_datetime(df['date'])
df['season'] = df['date'].apply(get_season)

# ######################################### DEFINE THE PAGES #####################################################################

### Intro page

if page == "Intro page":
    st.markdown("Currently, Citi Bike faces complaints regarding bike availability at certain times. This analysis aims to identify potential reasons behind these shortages. The dashboard is organized into four sections:")
    st.markdown("- **Most Popular Stations**: Highlighting stations with the highest usage.")
    st.markdown("- **Weather and Bike Usage**: Examining how weather conditions influence bike demand.")
    st.markdown("- **Interactive Map with Aggregated Trip Data**: Visualizing trip patterns and station activity.")
    st.markdown("- **Recommendations**: Suggesting strategic actions to improve bike availability.")
    st.markdown("Use the dropdown menu on the left labeled **'Analysis Menu'** to navigate between different sections of the analysis that our team has explored.")

    myImage = Image.open("CitiBike.jpg") 
    st.image(myImage, caption="Citi Bike Image")

### Most popular stations page

    # Create the season variable

elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['trip_count'].sum()) 
    st.metric(label='Total Bike Rides', value=f"{int(total_rides):,}")

    # Bar chart
    
    fig = go.Figure(go.Bar(
    x=top20['start_station_name'],
    y=top20['value'],
    marker={'color': top20['value'], 'colorscale': 'Blues'}
))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("The bar chart clearly highlights that certain start stations are significantly more popular than others. Notably, the top three stations are W 21 St & 6 Ave, Broadway & W 58 St, and West St & Chambers St. The substantial gap between the tallest and shortest bars indicates strong preferences for these leading stations. This insight can be further validated by cross-referencing with the interactive map accessible via the sidebar dropdown, allowing for a comprehensive understanding of station usage patterns.")

elif page == 'Weather and Bike Usage':

    ### Create the dual axis line chart page ###
    
    df_weather = pd.read_csv('trips_weather.csv', parse_dates=['date'])
    df_weather.sort_values('date', inplace=True)

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
        go.Scatter(
            x=df_weather['date'],
            y=df_weather['trip_count'],
            name='Daily Bike Rides',
            line=dict(color='blue')
        ),
        secondary_y=False
    )

    fig_2.add_trace(
        go.Scatter(
            x=df_weather['date'],
            y=df_weather['avgTemp'],
            name='Avg Temperature (Â°C)',
            line=dict(color='red')
        ),
        secondary_y=True
    )

    fig_2.update_layout(
        title='Bike Rides and Temperature Over Time in NYC',
        xaxis_title='Date',
        yaxis_title='Trip Count',
        yaxis2_title='Avg Temperature (Â°C)',
        legend=dict(x=0.01, y=0.99),
        plot_bgcolor='white',
        title_x=0.5
    )
    st.plotly_chart(fig_2, use_container_width=True)
    
    st.markdown("A clear correlation exists between daily temperature fluctuations and bike trip frequency. As temperatures drop, bike usage declines accordingly. This suggests that the bike shortage problem is likely more prominent during the warmer months, roughly from May to October, when bike demand is at its peak.")


elif page == 'Interactive Map with aggregated bike trips': 

    ### Add the Map ###
    st.write("Interactive Map showing aggregated bike trips over New York")

    path_to_html = "nyc-citibike.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

 ## Show in webpage
    st.header("Aggregated citi Bike Trips in New York")
    st.components.v1.html(html_data, height=1000)
    st.markdown("#### Using the filter on the left side of the map, we can verify whether the most popular start stations also feature among the most frequent trips.")
    st.markdown("**Busy Zones:** Areas like Midtown Manhattan, Central Park, and Downtown Manhattan exhibit exceptionally high trip volumes.")
    st.markdown("**Major Corridors:** Heavy bike traffic flows between key locations such as Union Square, Times Square, Central Park South, and Brooklyn waterfront.")
    st.markdown("**Possible Reasons:** These are densely populated regions with high commercial, tourist, and residential activity, leading to heavy use of bike sharing for commuting and leisure. Central Park, in particular, attracts many casual riders during summer.")
    st.markdown("**Interesting Observation:** Cross-borough trips, such as from Brooklyn to Manhattan, are less common than within-borough trips, likely due to challenges associated with crossing bridges.")


elif page == 'Conclusions and Recommendations':

    bikes = Image.open("business_pic.jpg")
    st.image(bikes, caption="Citi Bike Recommendations")

    st.markdown("### Our analysis identifies key factors contributing to bike shortages and uneven usage patterns across Citi Bike stations, along with recommended strategies to address them:")
    st.markdown("""
1. **Seasonal Variability:** Bike usage peaks during warmer months (May–October) and declines in colder months, driven by temperature fluctuations. Implementing seasonal redistribution plans can help mitigate shortages during peak demand periods.
2. **High-Demand Stations:** Stations like W 21 St & 6 Ave, West St & Chambers St, and Broadway & W 58 St experience high activity, leading to supply-demand imbalances. Introducing targeted rebalancing and incentivizing station usage can improve resource allocation.
3. **Regional Disparities:** Lower activity in outer boroughs suggests underutilization. Expanding service or marketing efforts in these areas can promote equitable usage.
4. **Connectivity Hotspots:** Strong travel links between Manhattan, Jersey City, and Brooklyn indicate a need for better infrastructure and data-driven bike redistribution to improve cross-borough travel efficiency.
5. **Redistribution Gaps:** Current operational strategies may be insufficient to handle demand fluctuations during peak seasons and at high-traffic stations. Investing in real-time demand monitoring and dynamic rebalancing can help reduce shortages.
""")
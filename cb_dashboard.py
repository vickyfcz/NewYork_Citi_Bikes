################################################ CITIBIKES DASHABOARD #####################################################
import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'Citi Bikes Strategy Dashboard', layout='wide')
st.title("Citi Bikes: Strategy Dashboard")
st.markdown("The dashboard will assist in addressing Citi Bike’s current expansion by providing clear insights into station usage, trip patterns, and potential areas for growth.")
st.markdown("""Citi Bike experiences availability issues at certain times, and this dashboard aims to identify the root causes of bike distribution inefficiencies, ensuring better allocation and availability to enhance customer satisfaction.""")


########################## Import data ###########################################################################################

df_analysis = pd.read_csv('subset_newyork_data.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)


# ######################################### DEFINE THE CHARTS #####################################################################

## Bar chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in NewYork',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width = True)


## Line chart 

# Aggregating the data by datetime
df_aggregated = df_analysis.groupby('date').agg({
    'trip_count': 'mean',  # Use 'mean' for daily bike rides
    'avgTemp': 'mean'  # Use 'mean' for daily temperature
}).reset_index()


# Creating subplot with two y-axes
fig_2 = make_subplots(specs=[[{"secondary_y": True}]])


# Adding trace for daily bike rides
fig_2.add_trace(
    go.Scatter(x=df_aggregated['date'], y=df_aggregated['trip_count'], name='Daily bike rides', line=dict(color='blue')),
    secondary_y=False,
)

# Adding trace for daily temperature
fig_2.add_trace(
    go.Scatter(x=df_aggregated['date'], y=df_aggregated['avgTemp'], name='Daily temperature', line=dict(color='red')),
    secondary_y=True,
)


# Updating layout
fig_2.update_layout(
    title='Daily bike rides and Temperature in 2022 New York',
    xaxis_title='Date',
    yaxis=dict(
        title='Daily Total Bike Rides',
        titlefont=dict(color='blue'),
        tickfont=dict(color='blue'),
        tickformat=".1s"
    ),
    yaxis2=dict(
        title='Daily Avg Temperature',
        titlefont=dict(color='red'),
        tickfont=dict(color='red'),
        anchor='x',
        overlaying='y',
        side='right',
        tickformat="d"
    ),
    legend=dict(
        x=0,
        y=1.1,
        orientation='h'
    ),
    height=600  
)

st.plotly_chart(fig_2, use_container_width=True)

### Add the map ###

path_to_html = "NewYork_CitiBike_Trips.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height=700)
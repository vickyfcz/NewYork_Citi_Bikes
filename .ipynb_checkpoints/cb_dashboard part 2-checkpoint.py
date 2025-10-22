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
st.title("Citi Bikes Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
    ["Intro page", "Weather component and bike usage",
     "Most popular stations",
     "Interactive map with aggregated bike trips", "Recommendations"])

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
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems Citi Bikes currently faces.")
    st.markdown("Right now, Citi bikes runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

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
from numerize import numerize
from PIL import Image
import plotly.express as px
import json

########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title='Citi Bikes Strategy Dashboard', layout='wide')
st.title("Citi Bikes Strategy Dashboard")

###  Define side bar
st.sidebar.title('Anaysis Menu')
page = st.sidebar.selectbox('Choose a section of the analysis',
                            ['Intro page',
                             'Weather and Bike Usage',
                             'Most popular stations',
                             'Interactive Map with aggregated bike trips',
                             'Classic versus electric bikes',
                             'Recommendations'])

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot.csv', index_col=0)

############################################ DEFINE THE PAGES #####################################################################

### Intro page

if page == "Intro page":
    
    st.markdown("#### This dashboard offers valuable insights to address the expansion challenges currently faced by New York Citi Bikes.")
st.markdown("Currently, Citi Bike users often report shortages and unavailability of bikes at certain times. This analysis explores the potential causes behind these issues. The dashboard is divided into five key sections:")
st.markdown('- **Weather and Usage Trends:** Examining how weather conditions influence bike demand.')
st.markdown('- **Most Popular Stations:** Identifying stations with the highest activity.')
st.markdown('- **Interactive Trip Map:** Visualizing aggregated bike trips across the city.')
st.markdown('- **Classic vs. Electric Bikes:** Comparing usage patterns between bike types.')
st.markdown('- **Recommendations:** Strategic suggestions to improve bike availability and distribution.')
st.markdown('Use the dropdown menu under **"Analysis Menu"** on the left to navigate through the different aspects of our analysis.')

myImage = Image.open("CitiBike.jpg")  # source: https://www.nyc.gov/office-of-the-mayor/news/576-18/mayor-de-blasio-dramatic-expansion-citi-bike#/0
st.image(myImage)

### Most popular stations page

    # Create the season variable

elif page == "Most popular stations":
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['trip_count'].sum()) 
    st.metric(label='Total Bike Rides', value=f"{int(total_rides):,}")
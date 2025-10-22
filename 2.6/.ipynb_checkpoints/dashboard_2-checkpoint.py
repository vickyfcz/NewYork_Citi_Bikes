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

    myImage = Image.open("CitiBike.jpg") 
    st.image(myImage, caption="Citi Bike Image")

### LINE CHART PAGE: WEATHER COMPONENT AND BIKE USAGE

elif page == 'Weather component and bike usage':

    # Aggregating the data by datetime
    df_aggregated = df.groupby('date').agg({
        'trip_count': 'mean',  # Use 'mean' for daily bike rides
        'avgTemp': 'mean'  # Use 'mean' for daily temperature
    }).reset_index()
    
    # Creating subplot with two y-axes
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    # Adding trace for daily bike rides
    fig2.add_trace(
        go.Scatter(x=df_aggregated['date'], y=df_aggregated['trip_count'], name='Daily bike rides', line=dict(color='blue')),
        secondary_y=False,
    )

    # Adding trace for daily temperature
    fig2.add_trace(
        go.Scatter(x=df_aggregated['date'], y=df_aggregated['avgTemp'], name='Daily temperature', line=dict(color='red')),
        secondary_y=True,
    )

    # Updating layout
    fig2.update_layout(
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

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")
    
    
### BAR CHART PAGE: MOST POPULAR STATIONS  

elif page == 'Most popular stations':  

    # Create the filter on the side bar
    with st.sidebar:
        season_filter = st.multiselect(label = 'Select the season', options = df['season'].unique(),
    default = df['season'].unique())

    df1 = df.query('season == @season_filter')

    # Define the total rides
    total_rides = float(df1['trip_count'].count())    
    st.metric(label = 'Total Bike Rides', value = numerize.numerize(total_rides))

    # Bar chart
     
    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
    
    fig.update_layout(
    title = 'Top 20 most popular bike stations in NYC 2022',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From the bar chart it is clear that there are some start stations that are more popular than others - in the top 3 are W 21 St & 6 Ave, West St & Chambers St, Broadway & W 58 St. There is a significant jump between the highest and lowest bars of the plot, indicating some clear preferences for the leading stations. This is a finding that we could cross reference with the interactive map with aggregated bike trips that you can access through the side bar select box.")
    
    
### MAP PAGE: INTERACTIVE MAP WITH AGGREGATED BIKE TRIPS

elif page == 'Interactive map with aggregated bike trips': 
    
    path_to_html = "NewYork_CitiBike_Trips.html" 

    # Read file and keep in variable
    with open(path_to_html, 'r') as f: 
        html_data = f.read()
        
    # Show in webpage
    st.header('Aggregated Bike Trips in NYC 2022')
    st.components.v1.html(html_data,height = 1000)
    st.markdown('#### Using the filter on the left hand side of the map, we can check whether the most popular start stations also appear in the most popular trips.')
    st.markdown("The most popular start stations are W 21 St & 6 Ave, West St & Chambers St, Broadway & W 58 St. While having the aggregated bike trips filter enabled, it is apparent that even though Broadway & W 58 St is a popular start station, it doesn't account for the most commonly taken trips.")
    st.markdown('Some of the most common routes are between West St/Chambers St,7 Ave & Central Park South, Grand Army Plaza & Central Park S,Soissons Landing which are located along the water, or routes located around the perimeter of Central Park.')


### HISTOGRAMS: CLASSIC VERSUS ELECTRIC BIKES

elif page == 'Classic versus electric bikes':

    # Ensure trip_count is numeric
    df['trip_count'] = pd.to_numeric(df['trip_count'], errors='coerce')

    # Ensure season is a categorical variable
    df['season'] = pd.Categorical(df['season'], categories=['winter', 'spring', 'summer', 'fall'], ordered=True)

    # Filter DataFrame by bike type
    classic_bike = df[df['rideable_type'] == 'classic_bike']
    electric_bike = df[df['rideable_type'] == 'electric_bike']

    # Count trip counts by season
    classic_counts = classic_bike.groupby('season')['trip_count'].count().reset_index()
    electric_counts = electric_bike.groupby('season')['trip_count'].count().reset_index()

    # Create the figure with subplots
    fig3 = make_subplots(rows=1, cols=1)

    # Add bar charts to the figure
    fig3.add_trace(go.Bar(
        x=classic_counts['season'],
        y=classic_counts['trip_count'],
        name='Classic Bike',
        marker=dict(color='blue')
    ), row=1, col=1)

    fig3.add_trace(go.Bar(
        x=electric_counts['season'],
        y=electric_counts['trip_count'],
        name='Electric Bike',
        marker=dict(color='green')
    ), row=1, col=1)

    # Update layout
    fig3.update_layout(
        title='Number of Trips by Bike Type Across Different Seasons',
        xaxis=dict(title='Season'),
        yaxis=dict(
            title='Number of Rentals',
            tickformat='.2s'  # Format large numbers with SI units (k, M, B)
        ),
        barmode='group',  # Group bars side by side
        height=600  # Adjust height if needed
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('The graph illustrates that classic bikes are rented significantly more often than electric bikes across all seasons. This suggests that classic bikes are generally more popular or more readily available. Electric bikes also see a slight increase in rentals as the temperature rises, but their rentals does not fluctuate as significantly as that of classic bikes.')
    st.markdown('Additionally, the data shows that classic bikes are rented over 2.8 times more often than electric bikes. This significant difference suggests limited availability of electric bikes, which could be a reason why their rentals does not vary much with the weather. So, the limited availability of electric bikes, makes them less accessible for customers to rent, regardless of the season.')
    
    
### CONCLUSIONS PAGE: RECOMMENDATIONS

else:
    
    st.header('Conclusions and Recommendations')
    bikes = Image.open("CitiBike_2.JPG")  # Source: https://gothamist.com/news/bigger-faster-and-flashier-new-e-bikes-join-citi-bikes-fleet
    st.image(bikes)
    st.markdown('Source: https://gothamist.com/news/bigger-faster-and-flashier-new-e-bikes-join-citi-bikes-fleet')
    st.markdown('### Our analysis has shown that NewYork CitiBikes should focus on the following objectives moving forward:')
    st.markdown('- There is a clear correlation between temperature and bike trips. Ensure that stations are fully stocked during the warmer months in order to meet the higher demand, but to provide a lower supply in winter and late autumn to reduce logistics cost.')
    st.markdown('- Adding bikes and bike parking spaces at the most popular stations, particularly those along the water and around Central Park.')
    st.markdown('- Increase the number of electric bikes in the fleet to better meet customer demand and improve accessibility.')
    st.markdown('- Ensure popular routes and stations are well-maintained for better user experience.')

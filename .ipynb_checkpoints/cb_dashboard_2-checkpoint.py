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


st.set_page_config(page_title = 'Citi Bikes Strategy Dashboard', layout='wide')
st.title("NY CitiBikes: Strategy Dashboard")
st.markdown("The dashboard will assist in addressing Citi Bike’s current expansion by providing clear insights into station usage, trip patterns, and potential areas for growth.")
st.markdown("""Citi Bike experiences availability issues at certain times, and this dashboard aims to identify the root causes of bike distribution inefficiencies, ensuring better allocation and availability to enhance customer satisfaction.""")

###  Define side bar
st.sidebar.title('Anaysis Menu')
page = st.sidebar.selectbox('Choose a section of the analysis',
                            ['Intro page',
                             'Weather and Bike Usage',
                             'Most popular stations',
                             'Interactive map with aggregated bike trips',
                             'Classic versus Electric Bikes',
                             'Recommendations'])

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot.csv', index_col=0)

# ######################################### DEFINE THE PAGES #####################################################################

### Intro page

if page == "Intro page":
    
    st.markdown("Currently, Citi Bike faces complaints regarding bike availability at certain times. This analysis aims to identify potential reasons behind these shortages. The dashboard is organized into four sections:")
    st.markdown("- **Most Popular Stations**: Highlighting stations with the highest usage.")
    st.markdown("- **Weather and Bike Usage**: Examining how weather conditions influence bike demand.")
    st.markdown("- **Interactive Map with Aggregated Trip Data**: Visualizing trip patterns and station activity.")
    st.markdown("- **Recommendations**: Suggesting strategic actions to improve bike availability.")
    st.markdown("Use the dropdown menu on the left labeled **'Anaysis Menu'** to navigate between different sections of the analysis that our team has explored.")

    myImage = Image.open("CitiBike.jpg")  # source: https://www.nyc.gov/office-of-the-mayor/news/576-18/mayor-de-blasio-dramatic-expansion-citi-bike#/0
    st.image(myImage)
    

## LINE CHART PAGE: WEATHER COMPONENT AND BIKE USAGE

elif page == 'Weather and Bike Usage':

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
        title=dict(
            text='Daily Total Bike Rides',
            font=dict(color='blue')
        ),
        tickfont=dict(color='blue'),
        tickformat=',d'
    ),
    yaxis2=dict(
        title=dict(
            text='Daily Avg Temperature',
            font=dict(color='red')
        ),
        tickfont=dict(color='red'),
        anchor='x',
        overlaying='y',
        side='right',
        tickformat='d'
    ),
    legend=dict(
        x=0,
        y=1.1,
        orientation='h'
    ),
    height=600
)

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("A clear correlation exists between daily temperature fluctuations and bike trip frequency. As temperatures decrease, bike usage correspondingly declines. This suggests that the bike shortage issue is likely most pronounced during the warmer months—roughly from May to October—when demand for bikes is at its highest.")

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
    st.markdown("The bar chart clearly shows that certain start stations are significantly more popular than others. The top three stations are W 21 St & 6 Ave, West St & Chambers St, and Broadway & W 58 St. The substantial gap between the tallest and shortest bars highlights strong preferences for these leading stations. This insight can be further validated by cross-referencing with the interactive map of aggregated bike trips accessible via the sidebar select box.")


### MAP PAGE: INTERACTIVE MAP WITH AGGREGATED BIKE TRIPS

elif page == 'Interactive map with aggregated bike trips': 
    
    path_to_html = "nyc-citibike.html" 

    # Read file and keep in variable
    with open(path_to_html, 'r') as f: 
        html_data = f.read()
        
    # Show in webpage
    st.header('Aggregated Bike Trips in NYC 2022')
    st.components.v1.html(html_data,height = 1000)
    st.markdown('#### Using the filter on the left side of the map, we can examine whether the most popular start stations also feature among the most frequently taken trips.')
    st.markdown("The most popular start stations include W 21 St & 6 Ave, West St & Chambers St, and Broadway & W 58 St. While the aggregated bike trips filter is active, it becomes evident that although Broadway & W 58 St is a highly used start station, it doesn't necessarily correspond to the most common trip routes.")
    st.markdown("Some of the most frequent routes connect Waterway-adjacent stations like West St/Chambers St, 7 Ave & Central Park South, Grand Army Plaza & Central Park S, and Soissons Landing. These routes tend to be along the water or around the perimeter of Central Park, indicating popular leisure and commuting paths around scenic and residential areas.")


### HISTOGRAMS: CLASSIC VERSUS ELECTRIC BIKES

elif page == 'Classic versus Electric Bikes':

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
    st.markdown('The graph demonstrates that classic bikes are rented significantly more often than electric bikes across all seasons, indicating that they are generally more popular or more widely available. While electric bike rentals show a slight increase with rising temperatures, their usage fluctuates much less than that of classic bikes, likely due to limited availability. Additionally, the data reveals that classic bikes are rented over 2.8 times more frequently than electric bikes. This substantial difference suggests that limited electric bike availability may be a key factor, making them less accessible to customers regardless of the season.')

### CONCLUSIONS PAGE: RECOMMENDATIONS

else:
    
    st.header('Conclusions and Recommendations')
    bikes = Image.open("business_pic.JPG")
    st.image(bikes)
    
    st.markdown('### Key Conclusions and Recommendations for New York CitiBikes Moving Forward:')
    st.markdown('- **Temperature and Demand Correlation:** There is a strong link between weather and bike trip volumes. To meet peak demand, stations should be fully stocked during warmer months, while reducing supply in winter and late autumn to optimize logistics and minimize costs. Implementing predictive analytics can further enhance supply chain efficiency by forecasting demand accurately.')
    st.markdown('- **Expansion at High-Traffic Locations:** Increasing the number of bikes and adding more bike parking spaces at the most popular stations—especially those along water-fronts and near Central Park—will help accommodate the high usage. Consider partnerships with local businesses to sponsor additional infrastructure improvements.')
    st.markdown('- **Boost Electric Bike Availability:** Expanding the electric bike fleet can better serve customer preferences and improve accessibility, particularly for longer or hilly routes. Introducing flexible rental options and subscription models for electric bikes can attract more users.')
    st.markdown('- **Maintain Popular Routes and Stations:** Regular maintenance and infrastructure improvements at key routes and stations will enhance the user experience and support sustainable growth. Consider introducing real-time monitoring of bike and station conditions can help ensure rapid response to maintenance needs.')
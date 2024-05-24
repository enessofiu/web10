import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import pytz
import time

# Title of the app
st.set_page_config(layout="wide")
st.title('Weather Dashboard')

# Load custom CSS
css_file_path = "styles.css"  # Ensure you have a CSS file named "styles.css" in the same directory
with open(css_file_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Function to construct the file path
def get_file_path(filename):
    return os.path.join(current_dir, filename)

# Define the filename
data_file = "predicted_data_2024.csv"

# Load dataset
df = pd.read_csv(get_file_path(data_file))

# Convert the timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set timezone to GMT+1
tz = pytz.timezone('Europe/Belgrade')  # Prizren is in the same timezone as Belgrade

# Function to get the current time in GMT+1
def get_current_time_gmt_plus_1():
    return datetime.now(tz)

# Filter data for the current date
def get_today_data(df, current_datetime):
    return df[df['timestamp'].dt.date == current_datetime.date()]

# Main dashboard function
def main():
    # Get current datetime in GMT+1
    current_datetime = get_current_time_gmt_plus_1()

    # Filter data for the current date
    df_today = get_today_data(df, current_datetime)

    # Extract the latest data point for current conditions
    if not df_today.empty:
        current_data = df_today.iloc[-1]
    else:
        st.error("No data available for today.")
        return

    # Current location
    current_location = 'Prizren, Kosovë'
    st.subheader(f'Current Location: {current_location}')

    # Weather icon and temperature
    col1, col2 = st.columns([3, 1])
    with col1:
        st.image('https://upload.wikimedia.org/wikipedia/commons/a/a6/Golden_Gate_Bridge_fog.JPG', use_column_width=True)
    with col2:
        st.markdown(f"### {current_data['TC_predicted']:.2f}°C")
        st.markdown(f"#### {current_datetime.strftime('%A, %I:%M %p')}")
        st.markdown('##### Partly Cloudy')

    # Today's Highlights
    st.subheader("Today's Highlights")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Precipitation", "2%")
    col2.metric("Humidity", f"{current_data['HUM_predicted']}%")
    col3.metric("Wind", "0 km/h")
    col4.metric("Sunrise & Sunset", "6:18 AM", "7:27 PM")

    # 3 Days Forecast
    st.subheader('3 Days Forecast')
    days = ['Tuesday', 'Wednesday', 'Thursday']
    forecast_data = {
        'Day': days,
        'TC_predicted': df['TC_predicted'][:3],
        'HUM_predicted': df['HUM_predicted'][:3],
        'PRES_predicted': df['PRES_predicted'][:3],
        'US_predicted': df['US_predicted'][:3],
        'SOIL1_predicted': df['SOIL1_predicted'][:3]
    }
    df_forecast = pd.DataFrame(forecast_data)
    
    for i in range(len(df_forecast)):
        st.markdown(f"{df_forecast['Day'][i]}")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.write(f"<div class='metric-container'><h4>Temperature</h4><div class='metric-value'>{df_forecast['TC_predicted'][i]:.2f}°C</div></div>", unsafe_allow_html=True)
        col2.write(f"<div class='metric-container'><h4>Humidity</h4><div class='metric-value'>{df_forecast['HUM_predicted'][i]:.2f}%</div></div>", unsafe_allow_html=True)
        col3.write(f"<div class='metric-container'><h4>Pressure</h4><div class='metric-value'>{df_forecast['PRES_predicted'][i]:.2f}</div></div>", unsafe_allow_html=True)
        col4.write(f"<div class='metric-container'><h4>US</h4><div class='metric-value'>{df_forecast['US_predicted'][i]:.2f}</div></div>", unsafe_allow_html=True)
        col5.write(f"<div class='metric-container'><h4>Soil</h4><div class='metric-value'>{df_forecast['SOIL1_predicted'][i]:.2f}</div></div>", unsafe_allow_html=True)

    # Temperature Analytics
    st.subheader('Temperature Analytics')
    df_today_resampled = df_today.set_index('timestamp').resample('3H').mean()  # Resample every 3 hours and compute mean

    fig, ax = plt.subplots(2)
    ax[0].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['TC_predicted'], marker='o')
    ax[1].plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['HUM_predicted'], marker='o')
    ax[0].set_ylabel('Temperature (°C)')
    ax[1].set_ylabel('Humidity (%)')
    st.pyplot(fig)

# Run the main function
if name == 'main':
    main()

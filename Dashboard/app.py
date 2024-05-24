import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import pytz
import time

# Titulli i aplikacionit
st.title('Weather Dashboard')

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Function to construct the file path
def get_file_path(filename):
    """
    Constructs the absolute path to the data file.

    Args:
        filename (str): The name of the data file (e.g., "predicted_data_2024.csv").

    Returns:
        str: The absolute path to the data file.
    """
    return os.path.join(current_dir, filename)

# Define the filename
data_file = "predicted_data_2024.csv"

# Load dataset
df = pd.read_csv(get_file_path(data_file))

# Convert the timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set timezone to GMT+2
tz = pytz.timezone('Europe/Bucharest')

# Function to get the current time in GMT+2
def get_current_time_gmt_plus_2():
    return datetime.now(tz)

# Filter data for the current date
def get_today_data(df, current_datetime):
    return df[df['timestamp'].dt.date == current_datetime.date()]

# Main dashboard function
def main():
    # Get current datetime in GMT+2
    current_datetime = get_current_time_gmt_plus_2()

    # Filter data for the current date
    df_today = get_today_data(df, current_datetime)

    # Extract the latest data point for current conditions
    if not df_today.empty:
        current_data = df_today.iloc[-1]
    else:
        st.error("No data available for today.")
        return

    # Lokacioni aktual
    current_location = 'Los Angeles, CA, USA'
    st.subheader(f'Current Location: {current_location}')

    # Ikona e motit dhe temperatura
    col1, col2 = st.columns([3, 1])
    with col1:
        st.image('https://upload.wikimedia.org/wikipedia/commons/a/a6/Golden_Gate_Bridge_fog.JPG', use_column_width=True)
    with col2:
        st.markdown(f"### {current_data['TC_predicted']:.2f}°C")
        st.markdown(f"#### {current_datetime.strftime('%A, %I:%M:%S %p')}")
        st.markdown('##### Partly Cloudy')

    # Pikat kryesore të ditës
    st.subheader("Today's Highlights")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Precipitation", "2%")  # Assuming constant, as no precipitation data in the dataset
    col2.metric("Humidity", f"{current_data['HUM_predicted']}%")
    col3.metric("Wind", "0 km/h")  # Assuming constant, as no wind data in the dataset
    col4.metric("Sunrise & Sunset", "6:18 AM", "7:27 PM")  # Assuming constant times

    # Parashikimi për 3 ditët e ardhshme
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
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric(df_forecast['Day'][i], f"{df_forecast['TC_predicted'][i]:.2f}°C")
        col2.metric("Humidity", f"{df_forecast['HUM_predicted'][i]}%")
        col3.metric("Pressure", f"{df_forecast['PRES_predicted'][i]:.2f}")
        col4.metric("US", f"{df_forecast['US_predicted'][i]:.2f}")
        col5.metric("Soil", f"{df_forecast['SOIL1_predicted'][i]:.2f}")

    # Analitika e temperaturës për ditën
    st.subheader('Temperature Analytics')
    df_today_resampled = df_today.set_index('timestamp').resample('3H').mean()  # Resample every 3 hours and compute mean

    fig, ax = plt.subplots()
    ax.plot(df_today_resampled.index.strftime('%I %p'), df_today_resampled['HUM_predicted'], marker='o')
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature (°C)')
    st.pyplot(fig)

    # Footer
    st.sidebar.header('Menu')
    st.sidebar.button('Home')
    st.sidebar.button('Forecast')
    st.sidebar.button('Locations')
    st.sidebar.button('Analytics')
    st.sidebar.button('Calendar')
    st.sidebar.button('Settings')

# Run the main function
if __name__ == '__main__':
    main()

# Automatically refresh the page every second to update the time display
while True:
    time.sleep(1)
    st.experimental_rerun()

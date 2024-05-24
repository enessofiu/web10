import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

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

# Get current datetime
current_datetime = datetime.now()

# Filter data for the current date
df_today = df[df['timestamp'].dt.date == current_datetime.date()]

# Extract the latest data point for current conditions
if not df_today.empty:
    current_data = df_today.iloc[-1]
else:
    st.error("No data available for today.")
    st.stop()

# Lokacioni aktual
current_location = 'Los Angeles, CA, USA'
st.subheader(f'Current Location: {current_location}')

# Ikona e motit dhe temperatura
col1, col2 = st.columns([3, 1])
with col1:
    st.image('https://upload.wikimedia.org/wikipedia/commons/a/a6/Golden_Gate_Bridge_fog.JPG', use_column_width=True)
with col2:
    st.markdown(f"### {current_data['TC_predicted']}°C")
    st.markdown(f"#### {current_datetime.strftime('%A, %I:%M %p')}")
    st.markdown('##### Partly Cloudy')

# Pikat kryesore të ditës
st.subheader("Today's Highlights")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Precipitation", "2%")  # Assuming constant, as no precipitation data in the dataset
col2.metric("Humidity", f"{current_data['HUM_predicted']}%")
col3.metric("Wind", "0 km/h")  # Assuming constant, as no wind data in the dataset
col4.metric("Sunrise & Sunset", "6:18 AM", "7:27 PM")  # Assuming constant times

# Grafikët e shansit për shi (Using dummy data as no rain data in the dataset)
st.subheader('Chance of Rain')
hours = ['09 AM', '12 PM', '03 PM', '06 PM', '09 PM', '12 AM', '03 AM']
chance_of_rain = [10, 20, 30, 50, 40, 20, 10]

fig, ax = plt.subplots()
ax.barh(hours, chance_of_rain, color='blue')
ax.set_xlabel('Chance of Rain (%)')
ax.set_ylabel('Time')
st.pyplot(fig)

# Parashikimi për 3 ditët e ardhshme (Using dummy data as no forecast data in the dataset)
st.subheader('3 Days Forecast')
forecast = {
    'Day': ['Tuesday', 'Wednesday', 'Thursday'],
    'Weather': ['Cloudy', 'Rainy', 'Snowfall'],
    'High': [26, 26, 26],
    'Low': [11, 11, 11]
}
df_forecast = pd.DataFrame(forecast)

for i in range(len(df_forecast)):
    col1, col2, col3 = st.columns(3)
    col1.metric(df_forecast['Day'][i], df_forecast['Weather'][i])
    col2.metric("High", f"{df_forecast['High'][i]}°C")
    col3.metric("Low", f"{df_forecast['Low'][i]}°C")

# Analitika e temperaturës për ditën
st.subheader('Temperature Analytics')
df_today = df_today.set_index('timestamp').resample('3H').mean()  # Resample every 3 hours and compute mean

fig, ax = plt.subplots()
ax.plot(df_today.index.strftime('%I %p'), df_today['TC_predicted'], marker='o')
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

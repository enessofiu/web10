import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Titulli i aplikacionit
st.title('Weather Dashboard')

# Lokacioni aktual
current_location = 'Los Angeles, CA, USA'
st.subheader(f'Current Location: {current_location}')

# Ikona e motit dhe temperatura
col1, col2 = st.columns([3, 1])
with col1:
    st.image('https://upload.wikimedia.org/wikipedia/commons/a/a6/Golden_Gate_Bridge_fog.JPG', use_column_width=True)
with col2:
    st.markdown('### 12°C')
    st.markdown('#### Monday, 07:43 AM')
    st.markdown('##### Partly Cloudy')

# Pikat kryesore të ditës
st.subheader("Today's Highlights")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Precipitation", "2%")
col2.metric("Humidity", "87%")
col3.metric("Wind", "0 km/h")
col4.metric("Sunrise & Sunset", "6:18 AM", "7:27 PM")

# Grafikët e shansit për shi
st.subheader('Chance of Rain')
hours = ['09 AM', '12 PM', '03 PM', '06 PM', '09 PM', '12 AM', '03 AM']
chance_of_rain = [10, 20, 30, 50, 40, 20, 10]

fig, ax = plt.subplots()
ax.barh(hours, chance_of_rain, color='blue')
ax.set_xlabel('Chance of Rain (%)')
ax.set_ylabel('Time')
st.pyplot(fig)

# Parashikimi për 3 ditët e ardhshme
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
hours = ['6 AM', '9 AM', '12 PM', '3 PM', '6 PM', '9 PM', '12 AM', '3 AM']
temperatures = [12, 14, 18, 22, 20, 16, 12, 10]

fig, ax = plt.subplots()
ax.plot(hours, temperatures, marker='o')
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

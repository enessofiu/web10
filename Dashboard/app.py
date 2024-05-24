import streamlit as st

# Placeholder data (replace with your actual data)
data = {
    'Temperature': 25,
    'Humidity': 60,
    'Pressure': 1013,
    'Soil Moisture': 75
}

# Page title and layout configuration
st.set_page_config(page_title="Weather Dashboard", layout="wide")

# Header section with search bar (currently non-functional)
header = st.container()
with header:
    st.title("Weather Dashboard")
    search_bar = st.text_input("Search Location", key="search")  # Placeholder search bar

# Data display section
data_section = st.container()
with data_section:
    # Titles for each data metric
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Temperature", f"{data['Temperature']} °C")
    col2.metric("Humidity", f"{data['Humidity']}%")
    col3.metric("Pressure", f"{data['Pressure']} hPa")
    col4.metric("Soil Moisture", f"{data['Soil Moisture']}%")

    # You can add charts or other data visualizations here

# Footer section
footer = st.container()
with footer:
    st.text("Created with Streamlit")


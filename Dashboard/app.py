import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Smart Agriculture Dashboard", layout="wide")

# Load custom CSS
css_file_path = os.path.join(os.path.dirname(__file__), "styles.css")
with open(css_file_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Function to construct the file path
def get_file_path(filename):
    return os.path.join(current_dir, filename)

# Cache the data loading function
@st.cache
def load_data(file_path):
    data = pd.read_csv(file_path)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    return data

# Function to calculate average values for today's date
def calculate_averages_today(data):
    today = datetime.now().date()
    today_data = data[data['timestamp'].dt.date == today]
    avg_values_today = {
        "TC": today_data["TC"].mean(),
        "HUM": today_data["HUM"].mean(),
        "PRES": today_data["PRES"].mean(),
        "US": today_data["US"].mean(),
        "SOIL1": today_data["SOIL1"].mean()
    }
    return avg_values_today

# Load the data
data = load_data(get_file_path('cleaned_data.csv'))
avg_values_today = calculate_averages_today(data)

# Predicted data for 2024 (example data)
predicted_data = pd.read_csv(get_file_path('predicted_data_2024.csv'))

# Get today's predicted averages if available
today_predicted_data = None
today_date_str = str(datetime.now().date())
if today_date_str in predicted_data['timestamp'].values:
    today_predicted_data = predicted_data[predicted_data['timestamp'] == today_date_str].iloc[0]

# Page title
st.title("Welcome to the Smart Agriculture Dashboard")

# Main content with average values
st.markdown(f"""
<div class="main">
    <div class="card-row">
        <div class="card-column">
            <div class="card" id="temp-card">
                <div class="icon">☀️</div>
                <h2>Temperature</h2>
                {f"<p id='temp-data'>Average: {today_predicted_data['TC']:.2f}°C</p>" if today_predicted_data is not None and not pd.isna(today_predicted_data['TC']) else "<p id='temp-data'>No data available</p>"}
            </div>
        </div>
        <div class="card-column">
            <div class="card" id="hum-card">
                <div class="icon">💧</div>
                <h2>Humidity</h2>
                {f"<p id='hum-data'>Average: {today_predicted_data['HUM']:.2f}%</p>" if today_predicted_data is not None and not pd.isna(today_predicted_data['HUM']) else "<p id='hum-data'>No data available</p>"}
            </div>
        </div>
        <div class="card-column">
            <div class="card" id="pres-card">
                <div class="icon">🌬️</div>
                <h2>Air Pressure</h2>
                {f"<p id='pres-data'>Average: {today_predicted_data['PRES']:.2f} hPa</p>" if today_predicted_data is not None and not pd.isna(today_predicted_data['PRES']) else "<p id='pres-data'>No data available</p>"}
            </div>
        </div>
    </div>
    <div class="card-row">
        <div class="card-column">
            <div class="card" id="us-card">
                <div class="icon">📡</div>
                <h2>Ultrasound</h2>
                {f"<p id='us-data'>Average: {today_predicted_data['US']:.2f}</p>" if today_predicted_data is not None and not pd.isna(today_predicted_data['US']) else "<p id='us-data'>No data available</p>"}
            </div>
        </div>
        <div class="card-column">
            <div class="card" id="soil-card">
                <div class="icon">🌱</div>
                <h2>Soil Moisture</h2>
                {f"<p id='soil-data'>Average: {today_predicted_data['SOIL1']:.2f}%</p>" if today_predicted_data is not None and not pd.isna(today_predicted_data['SOIL1']) else "<p id='soil-data'>No data available</p>"}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Visualization section title
st.header("Parameter Visualizations")

# Visualization section with sampling
st.markdown("<div class='main'>", unsafe_allow_html=True)

# Sample data for visualization to improve performance
sampled_data = data.sample(n=5000)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Temperature")
    st.line_chart(sampled_data.set_index('timestamp')['TC'])

    st.subheader("Humidity")
    st.line_chart(sampled_data.set_index('timestamp')['HUM'])

with col2:
    st.subheader("Air Pressure")
    st.line_chart(sampled_data.set_index('timestamp')['PRES'])

    st.subheader("Ultrasound")
    st.line_chart(sampled_data.set_index('timestamp')['US'])

    st.subheader("Soil Moisture")
    st.line_chart(sampled_data.set_index('timestamp')['SOIL1'])

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<footer>Smart Agriculture Dashboard © 2024</footer>", unsafe_allow_html=True)

# Javascript to handle hover effect and dynamic data
javascript = """
<script>
document.querySelectorAll('.card').forEach(item => {
    item.addEventListener('mouseover', event => {
        item.style.transform = 'rotateY(180deg)';
        item.style.transition = 'transform 0.5s ease';
    });

    item.addEventListener('mouseleave', event => {
        item.style.transform = 'rotateY(0deg)';
        item.style.transition = 'transform 0.5s ease';
    });
});

</script>
"""

st.markdown(javascript, unsafe_allow_html=True)

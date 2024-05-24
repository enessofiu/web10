import streamlit as st
import pandas as pd
import os





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
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    return data


# Cache the function to calculate average values
@st.cache_data
def calculate_averages(data):
    avg_values = {
        "TC": data["TC"].mean(),
        "HUM": data["HUM"].mean(),
        "PRES": data["PRES"].mean(),
        "US": data["US"].mean(),
        "SOIL1": data["SOIL1"].mean()
    }
    return avg_values



# Load the data
data = load_data(get_file_path('cleaned_data.csv'))
avg_values = calculate_averages(data)

# Page title
st.title("Welcome to the Smart Agriculture Dashboard")



# Main content with average values
st.markdown(f"""
<div class="main">
    <div class="card-row">
        <div class="card-column">
            <div class="card" onclick="navigateTo('/Temperature')">
                <div class="icon">☀️</div>
                <h2>Temperature</h2>
                <p>Average: {avg_values["TC"]:.2f}°C</p>
            </div>
        </div>
        <div class="card-column">
            <div class="card" onclick="navigateTo('/Humidity')">
                <div class="icon">💧</div>
                <h2>Humidity</h2>
                <p>Average: {avg_values["HUM"]:.2f}%</p>
            </div>
        </div>
        <div class="card-column">
            <div class="card" onclick="navigateTo('/Air_Pressure')">
                <div class="icon">🌬️</div>
                <h2>Air Pressure</h2>
                <p>Average: {avg_values["PRES"]:.2f} hPa</p>
            </div>
        </div>
    </div>
    <div class="card-row">
        <div class="card-column">
            <div class="card" onclick="navigateTo('/Ultrasound')">
                <div class="icon">📡</div>
                <h2>Ultrasound</h2>
                <p>Average: {avg_values["US"]:.2f}</p>
            </div>
        </div>
        <div class="card-column">
            <div class="card" onclick="navigateTo('/Soil_Moisture')">
                <div class="icon">🌱</div>
                <h2>Soil Moisture</h2>
                <p>Average: {avg_values["SOIL1"]:.2f}%</p>
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

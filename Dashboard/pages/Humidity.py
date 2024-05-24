import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Function to construct the file path
def get_file_path(filename):
    """
    Constructs the absolute path to the data file.

    Args:
        filename (str): The name of the data file (e.g., "cleaned_data.csv").

    Returns:
        str: The absolute path to the data file.
    """
    return os.path.join(current_dir, filename)

# Define the filename
data_file = "cleaned_data.csv"

def load_data(file_path):
    """
    Loads the data from the specified file path.

    Args:
        file_path (str): The absolute path to the data file.

    Returns:
        pandas.DataFrame: The loaded data as a pandas DataFrame.
    """
    return pd.read_csv(file_path)

# Load custom CSS
css_file_path = get_file_path("styles.css")
if os.path.exists(css_file_path):
    with open(css_file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.error(f"CSS file not found at path: {css_file_path}")

# Check if the data file exists before attempting to load it
data_path = get_file_path(data_file)
if os.path.exists(data_path):
    # Load the data using the function
    data = load_data(data_path)
    data['timestamp'] = pd.to_datetime(data['timestamp'])

    # Filter for Humidity (HUM)
    hum_data = data[['timestamp', 'HUM']]

    # Page title
    st.title("Humidity (HUM) Visualizations")

    # Arrange buttons in a single row
    col1, col2, col3, col4 = st.columns(4)

    # Button to show Line Chart
    if col1.button("Show Humidity Over Time"):
        st.markdown("<div class='card'><h3>Humidity Over Time</h3></div>", unsafe_allow_html=True)
        st.line_chart(hum_data.set_index('timestamp')['HUM'])

    # Button to show Bar Chart
    if col2.button("Show Humidity Distribution"):
        st.markdown("<div class='card'><h3>Humidity Distribution</h3></div>", unsafe_allow_html=True)
        st.bar_chart(hum_data.set_index('timestamp')['HUM'])

    # Button to show Pie Chart
    if col3.button("Show Humidity Proportions"):
        st.markdown("<div class='card'><h3>Humidity Proportions</h3></div>", unsafe_allow_html=True)
        hum_bins = pd.cut(hum_data['HUM'], bins=5)
        hum_pie_data = hum_bins.value_counts().reset_index()
        hum_pie_data.columns = ['Humidity Range', 'Count']  # Rename columns
        fig, ax = plt.subplots()
        ax.pie(hum_pie_data['Count'], labels=hum_pie_data['Humidity Range'], autopct='%1.1f%%')
        st.pyplot(fig)

    # Button to show Scatter Plot
    if col4.button("Show Humidity Scatter Plot"):
        st.markdown("<div class='card'><h3>Humidity Scatter Plot</h3></div>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        sns.scatterplot(x='timestamp', y='HUM', data=hum_data, ax=ax)
        st.pyplot(fig)

    st.markdown("<footer>Smart Agriculture Dashboard © 2024</footer>", unsafe_allow_html=True)
else:
    st.error(f"Data file not found at path: {data_path}")

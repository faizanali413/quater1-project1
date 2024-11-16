import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Streamlit configuration
st.set_page_config(
    layout="wide",  
    page_title="Weather Forecast", 
    page_icon="2.png", 
    initial_sidebar_state="auto" 
)

# Function to fetch weather data
def fetch_weather(city):
    try:
        url = f"https://www.weather-forecast.com/locations/{city}/forecasts/latest"
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        soup = BeautifulSoup(response.content, "lxml")
        
        # Extract temperature and condition
        temperature = soup.find("span", {"class": "temp"})
        condition = soup.find("span", {"class": "phrase"})
        
        if temperature and condition:
            return temperature.text.strip(), condition.text.strip()
        else:
            return None, None
    except requests.exceptions.RequestException:
        st.error(f"Failed to fetch data for {city}. Check your internet connection or try again later.")
        return None, None
    except AttributeError:
        st.error(f"Unable to fetch weather data for {city}. The website's structure may have changed.")
        return None, None

# Predefined cities
cities = {
    "Karachi": "karachi",
    "Lahore": "lahore",
    "Islamabad": "islamabad",
    "Peshawar": "peshawar",
    "Quetta": "quetta"
}

# Page header and design
st.markdown("<div style='height:10px; border-radius:50px; background-color: blue;'></div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Weather Forecast by Muhammad Usman</h1>", unsafe_allow_html=True)
st.markdown("<div style='height:10px; border-radius:50px; background-color: blue;'></div>", unsafe_allow_html=True)

# Layout: Image, city selection, and search input
col1, col2, col3 = st.columns(3)

with col1:
    # Check if the image file exists
    if os.path.exists("2.png"):
        st.image("2.png")
    else:
        st.warning("Image file '2.png' is missing.")

with col2:
    selected_cities = st.multiselect("Select Cities".upper(), list(cities.keys()))
    st.markdown("<div style='height:10px; background-color: blue;'></div>", unsafe_allow_html=True)

with col3:
    search_city = st.text_input("Search by City Name".upper())
    st.markdown("<div style='height:10px; background-color: blue;'></div>", unsafe_allow_html=True)

# Collect weather data
weather_data = []

# Fetch weather for selected predefined cities
for selected_city in selected_cities:
    city_code = cities[selected_city]
    temperature, condition = fetch_weather(city_code)
    if temperature and condition:
        weather_data.append({"City": selected_city, "Temperature": temperature, "Condition": condition})
    time.sleep(1)  # Pause to avoid overwhelming the server

# Fetch weather for the searched city
if search_city:
    city_code = search_city.lower().replace(" ", "-")
    temperature, condition = fetch_weather(city_code)
    if temperature and condition:
        weather_data.append({"City": search_city.title(), "Temperature": temperature, "Condition": condition})
    else:
        st.info(f"Weather data for {search_city.title()} is not available.")

# Display the weather data
if weather_data:
    df = pd.DataFrame(weather_data, columns=["City", "Temperature", "Condition"])
    st.markdown("<div style='height:10px; background-color: red;'></div>", unsafe_allow_html=True)
    st.table(df.set_index("City"))
    st.markdown("<div style='height:10px; background-color: blue;'></div>", unsafe_allow_html=True)
else:
    st.info("No weather data available. Please select or search for a city.")

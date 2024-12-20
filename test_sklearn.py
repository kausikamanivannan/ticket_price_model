# import streamlit as st
# import requests
# from datetime import datetime

# # Set up your API key
# API_KEY = "IqvAJBcdXQd2ySO7fh4k9Laa1M4AEJ0N"
# BASE_URL = "https://app.ticketmaster.com/discovery/v2/"

# # Streamlit app
# st.title("Ticketmaster Event Selector")

# # User input for event search
# artist_name = st.text_input("Enter artist name:")
# state_code = st.text_input("Enter state code (e.g., 'GA' for Georgia):")
# search_button = st.button("Search Events")

# if search_button:
#     # Construct the API URL
#     params = {
#         "apikey": API_KEY,
#         "keyword": artist_name,
#         "stateCode": state_code,
#         "classificationName": "Music"
#     }

#     response = requests.get(f"{BASE_URL}events.json", params=params)

#     if response.status_code == 200:
#         data = response.json()
#         events = data.get("_embedded", {}).get("events", [])

#         if events:
#             st.write(f"Found {len(events)} upcoming events:")

#             for event in events:
#                 # Event details
#                 name = event.get("name", "N/A")
#                 date = event.get("dates", {}).get("start", {}).get("localDate", "N/A")
#                 day_of_week = (
#                     datetime.strptime(date, "%Y-%m-%d").strftime("%A")
#                     if date != "N/A"
#                     else "N/A"
#                 )
#                 venue = event.get("_embedded", {}).get("venues", [{}])[0].get("name", "N/A")

#                 # Price details
#                 price_ranges = event.get("priceRanges", [{}])[0]
#                 min_price = price_ranges.get("min", "N/A")
#                 max_price = price_ranges.get("max", "N/A")
#                 currency = price_ranges.get("currency", "USD")

#                 if st.button(f"Select: {name} at {venue} on {date} ({day_of_week}) {min_price}"):
#                     st.session_state.selected_event = {
#                         "name": name,
#                         "date": date,
#                         "day_of_week": day_of_week,
#                         "venue": venue,
#                         "min_price": min_price,
#                         "max_price": max_price,
#                         "currency": currency,
#                     }
#                     st.experimental_rerun()
#         else:
#             st.write("No upcoming events found. Try a different search.")
#     else:
#         st.error(f"Error {response.status_code}: {response.text}")

# # Display selected event details
# if "selected_event" in st.session_state:
#     selected_event = st.session_state.selected_event
#     st.write("### Selected Event Details:")
#     st.write(f"- **Name**: {selected_event['name']}")
#     st.write(f"- **Date**: {selected_event['date']} ({selected_event['day_of_week']})")
#     st.write(f"- **Venue**: {selected_event['venue']}")
#     st.write(
#         f"- **Ticket Price**: {selected_event['min_price']} - {selected_event['max_price']} {selected_event['currency']}"
#     )


import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
import joblib

# Set up your API key
API_KEY = "IqvAJBcdXQd2ySO7fh4k9Laa1M4AEJ0N"
BASE_URL = "https://app.ticketmaster.com/discovery/v2/"

# Initialize the current page in session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Function to change the page
def change_page(page_name):
    st.session_state.current_page = page_name
    st.experimental_rerun()

# Define the Home Page
def home_page():
    st.title("Ticketmaster Event Selector")

    # User input for event search
    artist_name = st.text_input("Enter artist name:")
    state_code = st.text_input("Enter state code (e.g., 'GA' for Georgia):")
    search_button = st.button("Search Events")

    if search_button:
        # Construct the API URL
        params = {
            "apikey": API_KEY,
            "keyword": artist_name,
            "stateCode": state_code,
            "classificationName": "Music"
        }

        response = requests.get(f"{BASE_URL}events.json", params=params)

        if response.status_code == 200:
            data = response.json()
            events = data.get("_embedded", {}).get("events", [])

            if events:
                st.write(f"Found {len(events)} upcoming events:")

                for event in events:
                    name = event.get("name", "N/A")
                    date = event.get("dates", {}).get("start", {}).get("localDate", "N/A")
                    venue = event.get("_embedded", {}).get("venues", [{}])[0].get("name", "N/A")
                    min_price = event.get("priceRanges", [{}])[0].get("min", "N/A")

                    st.write(f"**Name**: {name}")
                    st.write(f"**Date**: {date}")
                    st.write(f"**Venue**: {venue}")
                    st.write(f"**Minimum Price**: ${min_price}")

                    if st.button(f"Select {name}", key=f"select_{name}_{date}"):
                        st.session_state.selected_event = {
                            "name": name,
                            "date": date,
                            "venue": venue,
                            "min_price": min_price
                        }
                        change_page("details")

            else:
                st.write("No upcoming events found. Try a different search.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")

# Define the Event Details Page
def details_page():
    st.title("Event Details and Prediction")

    if "selected_event" in st.session_state:
        selected_event = st.session_state.selected_event
        st.write("### Selected Event")
        st.write(f"- **Name**: {selected_event['name']}")
        st.write(f"- **Date**: {selected_event['date']}")
        st.write(f"- **Venue**: {selected_event['venue']}")
        st.write(f"- **Minimum Price**: ${selected_event['min_price']}")

        # Calculate days from event
        event_date = datetime.strptime(selected_event['date'], "%Y-%m-%d")
        days_from_event = (event_date - datetime.now()).days

        # Load the model and make a prediction
        try:
            model = joblib.load("random_forest_model.pkl")  # Ensure the model is saved as 'random_forest_model.pkl'
            features = pd.DataFrame({
                "days_from_event": [days_from_event],
                "min_price": [float(selected_event['min_price'])]
            })

            predicted_price = model.predict(features)[0]
            st.write(f"### Predicted Ticket Price: ${predicted_price:.2f}")

        except Exception as e:
            st.error(f"Error loading model or predicting price: {e}")

    else:
        st.write("No event selected. Please go back to the home page.")

    if st.button("Back to Home"):
        change_page("home")

# Render the current page
if st.session_state.current_page == "home":
    home_page()
elif st.session_state.current_page == "details":
    details_page()

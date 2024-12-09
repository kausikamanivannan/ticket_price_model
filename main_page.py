import streamlit as st
import requests
from datetime import datetime

# Set up your API key
API_KEY = "IqvAJBcdXQd2ySO7fh4k9Laa1M4AEJ0N"
BASE_URL = "https://app.ticketmaster.com/discovery/v2/"

# Streamlit app
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

            for index, event in enumerate(events):
                # Event details
                name = event.get("name", "N/A")
                date = event.get("dates", {}).get("start", {}).get("localDate", "N/A")
                day_of_week = (
                    datetime.strptime(date, "%Y-%m-%d").strftime("%A")
                    if date != "N/A"
                    else "N/A"
                )
                venue = event.get("_embedded", {}).get("venues", [{}])[0].get("name", "N/A")

                # Price details
                price_ranges = event.get("priceRanges", [{}])[0]
                min_price = price_ranges.get("min", "N/A")
                max_price = price_ranges.get("max", "N/A")
                currency = price_ranges.get("currency", "USD")

                if st.button(f"Select Event {index+1}"):
                    st.session_state.selected_event = {
                        "name": name,
                        "date": date,
                        "day_of_week": day_of_week,
                        "venue": venue,
                        "min_price": min_price,
                        "max_price": max_price,
                        "currency": currency,
                    }
                    st.experimental_set_query_params(page="details")
                    st.experimental_rerun()
        else:
            st.write("No upcoming events found. Try a different search.")
    else:
        st.error(f"Error {response.status_code}: {response.text}")

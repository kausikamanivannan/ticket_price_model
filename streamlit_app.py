import streamlit as st
import requests

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

                    if st.button(f"Select: {name} at {venue} on {date}"):
                        st.session_state.selected_event = {
                            "name": name,
                            "date": date,
                            "venue": venue
                        }
                        change_page("next")  # Navigate to the next page
            else:
                st.write("No upcoming events found. Try a different search.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")


# Define the Next Page
def next_page():
    st.title("Selected Event Details")

    # Display selected event details
    if "selected_event" in st.session_state:
        selected_event = st.session_state.selected_event
        st.write("### Selected Event")
        st.write(f"- **Name**: {selected_event['name']}")
        st.write(f"- **Date**: {selected_event['date']}")
        st.write(f"- **Venue**: {selected_event['venue']}")
        st.write("Done")
    else:
        st.write("No event selected. Please go back to the home page.")

    # Button to go back to the home page
    if st.button("Back to Home"):
        change_page("home")

# Render the current page
if st.session_state.current_page == "home":
    home_page()
elif st.session_state.current_page == "next":
    next_page()

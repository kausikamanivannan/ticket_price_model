import streamlit as st
import requests

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
                    st.experimental_rerun()
        else:
            st.write("No upcoming events found. Try a different search.")
    else:
        st.error(f"Error {response.status_code}: {response.text}")

# Check if an event has been selected
if "selected_event" in st.session_state:
    st.write("### Selected Event")
    selected_event = st.session_state.selected_event
    st.write(f"- **Name**: {selected_event['name']}")
    st.write(f"- **Date**: {selected_event['date']}")
    st.write(f"- **Venue**: {selected_event['venue']}")
    st.write("Done")



# import streamlit as st
# import requests

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
#                 name = event.get("name", "N/A")
#                 date = event.get("dates", {}).get("start", {}).get("localDate", "N/A")
#                 venue = event.get("_embedded", {}).get("venues", [{}])[0].get("name", "N/A")

#                 if st.button(f"Select: {name} at {venue} on {date}"):
#                     st.session_state.selected_event = {
#                         "name": name,
#                         "date": date,
#                         "venue": venue
#                     }
#                     st.experimental_rerun()
#         else:
#             st.write("No upcoming events found. Try a different search.")
#     else:
#         st.error(f"Error {response.status_code}: {response.text}")

# # Check if an event has been selected
# if "selected_event" in st.session_state:
#     st.write("### Selected Event")
#     selected_event = st.session_state.selected_event
#     st.write(f"- **Name**: {selected_event['name']}")
#     st.write(f"- **Date**: {selected_event['date']}")
#     st.write(f"- **Venue**: {selected_event['venue']}")

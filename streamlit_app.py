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
                        "id": event.get("id"),
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

    # Fetch detailed event information
    event_id = selected_event['id']
    st.write(f"Fetching details for event ID: {event_id}")  # Debugging message
    detail_response = requests.get(f"{BASE_URL}events/{event_id}.json", params={"apikey": API_KEY})

    if detail_response.status_code == 200:
        detail_data = detail_response.json()
        st.write("Detailed event data fetched successfully!")  # Debugging message

        # Display additional details
        st.write("### Event Details")

        # Artists/Performers
        performers = detail_data.get("_embedded", {}).get("attractions", [])
        if performers:
            st.write("**Artists/Performers:**")
            for performer in performers:
                st.write(f"- {performer.get('name', 'N/A')}")
        else:
            st.write("No artist information available.")

        # Ticket Prices
        price_ranges = detail_data.get("priceRanges", [])
        if price_ranges:
            st.write("**Ticket Prices:**")
            for price_range in price_ranges:
                min_price = price_range.get("min", "N/A")
                max_price = price_range.get("max", "N/A")
                currency = price_range.get("currency", "USD")
                st.write(f"- {min_price} - {max_price} {currency}")
        else:
            st.write("No ticket price information available.")

        # Additional Event Info
        info = detail_data.get("info", "N/A")
        if info:
            st.write("**Additional Info:**")
            st.write(info)
    else:
        st.error(f"Error {detail_response.status_code}: {detail_response.text}")
        st.write("### Debugging Info")
        st.json(detail_response.json())


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

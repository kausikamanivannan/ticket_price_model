import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Load the processed data and model setup
processed_data_path = 'ProcessedTicketData.csv'
data = pd.read_csv(processed_data_path)
data['date'] = pd.to_datetime(data['date'], utc=True)

target = 'max_price'
features = data.drop(columns=['event_id', 'max_price'])

# Encode categorical columns
encoders = {}
for col in ['artist', 'venue', 'city', 'state', 'ticket_vendor']:
    if col in features:
        encoder = LabelEncoder()
        features[col] = encoder.fit_transform(data[col])
        encoders[col] = encoder


############################################################################################################
# Ensure 'days_since_epoch' is numeric and drop the 'date' column if present
if 'date' in features:
    features = features.drop(columns=['date'])

features['days_since_epoch'] = (data['date'] - pd.Timestamp("1970-01-01")).dt.total_seconds() / (60 * 60 * 24)
############################################################################################################


X = features
y = data[target]

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Streamlit app setup
st.title("Ticketmaster Event Selector with Ticket Price Prediction")

# User input for event search
artist_name = st.text_input("Enter artist name:")
state_code = st.text_input("Enter state code (e.g., 'GA' for Georgia):")
search_button = st.button("Search Events")

if search_button:
    # Construct the API URL
    API_KEY = "IqvAJBcdXQd2ySO7fh4k9Laa1M4AEJ0N"
    BASE_URL = "https://app.ticketmaster.com/discovery/v2/"
    params = {
        "apikey": API_KEY,
        "keyword": artist_name,
        "stateCode": state_code,
        "classificationName": "Music"
    }

    try:
        response = requests.get(f"{BASE_URL}events.json", params=params)
        response.raise_for_status()
        data = response.json()
        events = data.get("_embedded", {}).get("events", [])

        if events:
            st.write(f"Found {len(events)} upcoming events:")
            for idx, event in enumerate(events):
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
    except Exception as e:
        st.error(f"Failed to fetch events: {e}")

# Event prediction logic
if "selected_event" in st.session_state:
    selected_event = st.session_state.selected_event
    st.write("### Selected Event")
    st.write(f"- **Name**: {selected_event['name']}")
    st.write(f"- **Date**: {selected_event['date']}")
    st.write(f"- **Venue**: {selected_event['venue']}")

    # Predict ticket prices
    try:
        event_date = datetime.strptime(selected_event['date'], '%Y-%m-%d')
        today = datetime.now()
        if event_date < today:
            st.write("The selected event date has already passed. Prediction not available.")
        else:
            days_until_event = (event_date - today).days
            prediction_dates = [today + timedelta(days=i) for i in range(days_until_event + 1)]
            
            predicted_prices = []
            for prediction_date in prediction_dates:
                features_sample = X.iloc[0].copy()
                if artist_name in encoders['artist'].classes_:
                    features_sample['artist'] = encoders['artist'].transform([artist_name])[0]
                else:
                    st.error(f"Artist '{artist_name}' not found in the model training data.")
                    break
                features_sample['days_since_epoch'] = (prediction_date - datetime(1970, 1, 1)).days
                predicted_prices.append(model.predict([features_sample.values])[0])

            # Find minimum price and corresponding date
            min_price = min(predicted_prices)
            min_price_date = prediction_dates[predicted_prices.index(min_price)]

            st.write(f"### Predicted Ticket Prices")
            st.write(f"- **Minimum Price**: ${min_price:.2f} on {min_price_date.strftime('%Y-%m-%d')}")

            # Plot the prices
            fig, ax = plt.subplots()
            ax.plot(prediction_dates, predicted_prices, label='Predicted Prices')
            ax.axvline(min_price_date, color='red', linestyle='--', label='Minimum Price Date')
            ax.set_title("Predicted Ticket Prices Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price ($)")
            ax.legend()
            st.pyplot(fig)
    except Exception as e:
        st.error(f"Prediction failed: {e}")

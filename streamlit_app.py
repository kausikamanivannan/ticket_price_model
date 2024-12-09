import streamlit as st
import pandas as pd
import datetime
import math
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# from google.colab import drive
# drive.mount('/content/drive')

data = pd.read_csv('ProcessedTicketData.csv')
print(f"Features shape: {data.shape}")

# Convert 'date' column to string, take first 10 characters, and convert to datetime
data['date'] = data['date'].astype(str).str[:10]
data['date'] = pd.to_datetime(data['date'])

print(data['date'].head(10))  # first 10 rows of the date column

# Target variable
target = 'max_price'

# Drop the target column to get only the features
features = data.drop(columns=['event_id', 'max_price'])

# Dictionary to store encoders for each column
encoders = {}

# Encode categorical columns
for col in ['artist', 'venue', 'city', 'state', 'ticket_vendor']:
    if col in features:
        encoder = LabelEncoder()
        features[col] = encoder.fit_transform(data[col])
        encoders[col] = encoder

print(f"Features shape: {features.shape}")

print(features.head())

# Splitting the data in test and train datasets

X = features
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # 20% train data, 20% test data

print(f"Training set size: {X_train.shape}")
print(f"Testing set size: {X_test.shape}")

# Extract year, month, day, and day_of_week from the date column for train and test

if 'date' in X_train.columns:
    X_train['year'] = X_train['date'].dt.year
    X_train['month'] = X_train['date'].dt.month
    X_train['day'] = X_train['date'].dt.day
    X_train['day_of_week'] = X_train['date'].dt.dayofweek
    X_train['days_since_epoch'] = (X_train['date'] - pd.Timestamp('1970-01-01')).dt.days

    X_test['year'] = X_test['date'].dt.year
    X_test['month'] = X_test['date'].dt.month
    X_test['day'] = X_test['date'].dt.day
    X_test['day_of_week'] = X_test['date'].dt.dayofweek
    X_test['days_since_epoch'] = (X_test['date'] - pd.Timestamp('1970-01-01')).dt.days

    # Drop the original date column
    X_train = X_train.drop(columns=['date'])
    X_test = X_test.drop(columns=['date'])

# train random forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate evaluation metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse}")
print(f"R^2 Score: {r2}")

# Mock predict_ticket_price function for demonstration
def predict_ticket_price(days_from_event, ticket_price):
    # Simulate a decrease in ticket price as the event approaches
    days_from_event = pd.to_datetime(days_from_event)
    predicted_price = max(10, ticket_price - (0.5 * days_from_event)) + random.uniform(-5, 5)
    return f"Predicted ticket price: ${predicted_price:.2f}"
    st.write(f"Predicted ticket price: ${predicted_price:.2f}")

# # Function to predict ticket prices per day leading up to the event
# def predict_ticket_price_per_day(event_date, ticket_price):
#     current_date = pd.Timestamp.now()
#     days_range = (event_date - current_date).days
#     prices = []
#     dates = []

#     for days_from_event in range(days_range + 1):
#         predicted_price = predict_ticket_price(days_from_event, ticket_price)
#         if predicted_price:
#             prices.append(float(predicted_price.split("$")[1]))
#             dates.append(current_date + pd.Timedelta(days=days_from_event))

#     return dates, prices

# # Event date and ticket price setup
# #event_date = pd.Timestamp('2024-12-25')
# ticket_price = int(input("Enter the current ticket price: ")) #50.00
# import pandas as pd

# # Function to get and validate user input
# def get_event_date():
#     while True:
#         user_input = input("Enter the event date in the format YYYY-MM-DD: ")
#         try:
#             # Convert the input string to a pandas Timestamp
#             event_date = pd.Timestamp(user_input)
#             print(f"Event date is set to: {event_date}")
#             return event_date
#         except ValueError:
#             print("Invalid date format! Please try again.")

# # Call the function
# event_date = get_event_date()


# dates, prices = predict_ticket_price_per_day(event_date, ticket_price)

# # Find the lowest price and the corresponding date
# lowest_price = min(prices)
# lowest_price_date = dates[prices.index(lowest_price)]

# print(f"Lowest price: ${lowest_price:.2f} on {lowest_price_date.date()}")

# Plot the prices over time
# plt.figure(figsize=(10, 6))
# plt.plot(dates, prices, label='Predicted Ticket Price', marker='o')
# plt.axvline(x=lowest_price_date, color='red', linestyle='--', label='Lowest Price')
# plt.title("Predicted Ticket Prices Leading Up to the Event")
# plt.xlabel("Date")
# plt.ylabel("Predicted Ticket Price ($)")
# plt.legend()
# plt.grid()
# plt.show()


# Streamlit App
def main():
    st.title("Concert Ticket Price Predictor")

    # User input for Artist and Venue
    day_of_concert = st.text_input("Enter Day of Concert YYYY-MM-DD")
    current_ticket_price = st.text_input("Enter Ticket Price")

    # Predict button and price display
    if st.button("Predict Price"):
        predict_ticket_price(day_of_concert, current_ticket_price)

if __name__ == "__main__":
    main()


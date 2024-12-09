import streamlit as st
import pandas as pd
import datetime
import math
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt






# Streamlit App
def main():
    st.title("Concert Ticket Price Predictor")

    # User input for Artist and Venue
    day_of_concert = st.text_input("Enter Day of Concert")
    current_ticket_price = st.text_input("Enter Ticket Price")

    # Predict button and price display
    if st.button("Predict Price"):
        predict_ticket_price(day_of_concert, current_ticket_price)

if __name__ == "__main__":
    main()


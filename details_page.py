import streamlit as st

# Check if selected_event is in session_state
if "selected_event" not in st.session_state:
    st.error("No event selected. Please go back to the main page and select an event.")
    st.stop()

selected_event = st.session_state.selected_event

# Display event details
st.title("Event Details")
st.write("### Selected Event Details:")
st.write(f"- **Name**: {selected_event['name']}")
st.write(f"- **Date**: {selected_event['date']} ({selected_event['day_of_week']})")
st.write(f"- **Venue**: {selected_event['venue']}")
st.write(
    f"- **Ticket Price**: {selected_event['min_price']} - {selected_event['max_price']} {selected_event['currency']}"
)

st.button("Go Back", on_click=lambda: st.experimental_set_query_params(page="main"))

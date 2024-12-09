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

import streamlit as st
from utils import post_daily_input
from datetime import date

st.title("Daily Input")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in from the home page.")
else:
    input_date = st.date_input("Date", value=date.today())
    input_data = st.number_input("How many poopikins did you do today and what were they like?")
    poop_type = st.selectbox("What type of poopikins did you do today?", ["Soft", "Hard", "Liquid", "Other"])
    poop_color = st.selectbox("What color was your poopikins?", ["Yellow", "Green", "Brown", "Black", "Red", "Orange", "White", "Other"])
    poop_size = st.selectbox("What size was your poopikins?", ["Small", "Medium", "Large", "Other"])

    if st.button("Submit Daily Input"):
        response = post_daily_input(str(input_date), input_data, poop_type, poop_color, poop_size)
        if response is None:
            # Error message is already shown by post_daily_input
            pass
        elif response.status_code == 200:
            st.success("Daily input saved!")
        else:
            st.error("Failed to save input.")

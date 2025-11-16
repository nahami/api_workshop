import streamlit as st
import requests
import json

st.sidebar.title("navigatie")

st.title("API Demo")

geturlmetparam = "https://api.aladhan.com/v1/timingsByCity/09-11-2025?city=Amsterdam&country=NL&method=13&shafaq=general&tune=5%2C3%2C5%2C7%2C9%2C-1%2C0%2C8%2C-6&school=0&timezonestring=Europe%2FAmsterdam&calendarMethod=DIYANET"

datajson = requests.get(geturlmetparam).json()


st.write(datajson)
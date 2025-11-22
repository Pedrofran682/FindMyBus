import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen

st.set_page_config(page_title="Find My Bus",
                   layout="wide")


m = folium.Map(location=[-22.9068, -43.1729], zoom_start=16)
st_data = st_folium(m, use_container_width=True,)

# Using "with" notation
with st.sidebar:
    st.text_input("Número do ônibus")
    st.selectbox("Click me",options=["a", "b", "c", "z"])

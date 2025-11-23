import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen

st.set_page_config(page_title="Find My Bus",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   page_icon="src/findmybus/assets/imgs/Logo.png"   )
st.logo("src/findmybus/assets/imgs/Logo_Name.png", 
        icon_image="src/findmybus/assets/imgs/Logo.png")

with st.sidebar:
    st.title("Find My Bus")
    st.text_input("Número do ônibus")
    st.selectbox("Click me",options=["a", "b", "c", "z"])


m = folium.Map(location=[-22.9068, -43.1729], zoom_start=816)
fg = folium.FeatureGroup(name="Markers")

st_folium(
    m,
    key="new",
    feature_group_to_add=fg,
    use_container_width=True
)
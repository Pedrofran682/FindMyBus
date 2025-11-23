import streamlit as st
import folium
from streamlit_folium import st_folium

from findmybus.ui.utils import get_fg_bus_location

st.set_page_config(page_title="Find My Bus",
                   layout="wide",
                   initial_sidebar_state="expanded"  )

with st.sidebar:
    st.title("Find My Bus")
    line = st.text_input("Número do ônibus", 
                         placeholder="Ex: 457",
                         max_chars=20)
    if st.button("Buscar"):
        st.rerun()

# TODO: Verify bettler tiles
# attr = (
#     '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
#     'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
# )
# tiles = "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png"
# folium.Map(location=[lat, lon], tiles=tiles, attr=attr, zoom_start=zoom_start)

map = folium.Map(location=[-22.908690, -43.210514],
                 zoom_start=14,
                 tiles="Cartodb Positron")
fg = get_fg_bus_location(line)
st_folium(
    map,
    feature_group_to_add=fg,
    use_container_width=True
)
import streamlit as st
import folium
from streamlit_folium import st_folium
from findmybus.ui.utils import get_bus_info

st.set_page_config(page_title="Cadê meu busão?",
                   layout="wide",
                   initial_sidebar_state="expanded"  )

with st.sidebar:
    st.title("Cadê meu busão?")
    line = st.text_input("Número do ônibus", 
                         placeholder="Ex: 457",
                         max_chars=20)
    fg_group, display_info = get_bus_info(line)
    if st.button("Buscar"):
        st.rerun()
    if display_info:
        for index, destination in enumerate(display_info["destination"]):
            st.badge(destination, color=display_info["color"][index])


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

st_folium(
    map,
    feature_group_to_add=fg_group,
    use_container_width=True
)
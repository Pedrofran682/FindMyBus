from sqlalchemy import Sequence
import streamlit as st
from findmybus.Models.orm import Positions
from findmybus.database.Connector import Connector
import folium
from sqlalchemy.engine import Engine
from functools import lru_cache
from findmybus.database.dbActions import get_buses_position


@lru_cache()
def _get_marker_symbol():
    icon_path = "src/findmybus/config/assets/imgs/bus-station.png"
    return folium.features.CustomIcon(icon_image=icon_path)


@st.cache_resource(ttl=600)
def get_db_engine() -> Engine:
    conn = Connector()
    return conn.get_db_engine()


@st.cache_resource(ttl=60)
def get_fg_bus_location(line: str) -> folium.FeatureGroup:
    positions = get_buses_position(get_db_engine(), line)
    marker_group = folium.FeatureGroup(name="BusPosition")

    for bus_position in positions:
        marker_group.add_child(
            folium.Marker(
                location=[bus_position.latitude, bus_position.longitude],
                tooltip=f"Linha: {bus_position.line}",
                popup=f"Velocidade: {bus_position.velocity} km/s",
            )
        )
    return marker_group
from sqlalchemy import Sequence
import streamlit as st
from findmybus.Models.orm import Positions
from findmybus.database.Connector import Connector
import folium
from sqlalchemy.engine import Engine
from functools import lru_cache
from findmybus.database.dbActions import get_buses_position, get_bus_route


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


@st.cache_resource(ttl=(60 * 30))
def get_fg_bus_route(line: str) -> folium.FeatureGroup:
    routes = get_bus_route(get_db_engine(), line)
    display_info = {"destination":[],
                    "color": []}
    polyLine_route_group = folium.FeatureGroup(name="BusRoute")
    colors = ["red", "blue", "green", "orange"]
    for index, route in enumerate(routes):
        locations = [[p[1], p[0]] for p in route.geometry["coordinates"]]
        route_line = folium.PolyLine(
            locations=locations,
            color=colors[index],
            weight=3,
            tooltip=route.destination
            )
        polyLine_route_group.add_child(route_line)
        display_info["destination"].append(route.destination)
        display_info["color"].append(colors[index])
    return polyLine_route_group, display_info


@st.cache_resource(ttl=60)
def get_bus_info(line: str):
    fg_bus_position = get_fg_bus_location(line)
    fg_route, display_info = get_fg_bus_route(line)
    fg_group = [fg_bus_position, fg_route]
    return fg_group, display_info
import streamlit as st
from findmybus.database.Connector import Connector
import folium
from sqlalchemy.engine import Engine
from functools import lru_cache
from findmybus.database.dbActions import get_buses_position, get_bus_route
from datetime import datetime


@lru_cache()
def _get_marker_symbol():
    icon_path = "src/findmybus/config/assets/imgs/BusSymbolBlack.png" 
    return folium.CustomIcon(
        icon_image=icon_path,
        icon_size=(24,24))


@st.cache_resource(ttl=600)
def get_db_engine() -> Engine:
    conn = Connector()
    return conn.get_db_engine()

def unixTime2DateTime(unixTime: int): return datetime.fromtimestamp(int(unixTime)/ 1000)

def get_diff_time_status(bus_unixTime: int) -> str:
    postion_time = unixTime2DateTime(bus_unixTime)
    now = datetime.now()
    delta = (now - postion_time).total_seconds() 
    if (delta / 60) < 1:
        return f"Atrasado em {delta}"
    return f"Atualizado em {delta} s"

@st.cache_resource(ttl=60)
def get_fg_bus_location(line: str) -> folium.FeatureGroup:
    positions = get_buses_position(get_db_engine(), line)
    marker_group = folium.FeatureGroup(name="BusPosition")
    for bus_position in positions:
        status = get_diff_time_status(bus_position.dateTime)
        popup_message = f"Velocidade: {bus_position.velocity} km/s<br>Status: {status}"
        marker_group.add_child(
            folium.Marker(
                location=[bus_position.latitude, bus_position.longitude],
                tooltip=f"Linha: {bus_position.line}",
                popup=popup_message,
                icon=_get_marker_symbol()
            )
        )
    return marker_group

COLORS = ["red", "blue"]
@st.cache_resource(ttl=(60 * 30))
def get_fg_bus_route(line: str) -> folium.FeatureGroup:
    routes = get_bus_route(get_db_engine(), line)
    display_info = {"destination":[],
                    "color": []}
    polyLine_route_group = folium.FeatureGroup(name="BusRoute")
    for index, route in enumerate(routes):
        if index == 2: break
        locations = [[p[1], p[0]] for p in route.geometry["coordinates"]]
        route_line = folium.PolyLine(
            locations=locations,
            color=COLORS[index],
            weight=3,
            tooltip=route.destination
            )
        polyLine_route_group.add_child(route_line)
        display_info["destination"].append(route.destination)
        display_info["color"].append(COLORS[index])
    return polyLine_route_group, display_info


@st.cache_resource(ttl=60)
def get_bus_info(line: str):
    fg_bus_position = get_fg_bus_location(line)
    fg_route, display_info = get_fg_bus_route(line)
    fg_group = [fg_bus_position, fg_route]
    return fg_group, display_info
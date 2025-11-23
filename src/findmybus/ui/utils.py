import streamlit as st
from findmybus.database.Connector import Connector

@st.cache_resource(ttl=600)
def get_db_connector() -> Connector:
    return Connector()
import streamlit as st
import pandas as pd
import geopandas
import shapely.geometry
import folium
import requests

APP_TITLE = 'Κ.Ο.Μ.Υ. backend'
APP_SUB_TITLE = 'by CMT Prooptiki'

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)
    st.file_uploader("Επελεξε περιφεριες", type=["xlsx"], key="key1")
    st.file_uploader("Επελεξε περιφεριακες ενοτητες", type=["xlsx"], key="key2")
if __name__ == "__main__":
    main()
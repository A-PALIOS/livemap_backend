import streamlit as st
import pandas as pd

APP_TITLE = 'Κ.Ο.Μ.Υ. backend'
APP_SUB_TITLE = 'by CMT Prooptiki'

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

if __name__ == "__main__":
    main()
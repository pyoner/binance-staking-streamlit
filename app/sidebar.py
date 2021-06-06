import streamlit as st
from os.path import dirname, join


def get_sidebar_data():
    f_name = join(dirname(__file__), './sidebar.md')

    with open(f_name) as f:
        return ''.join(f.readlines())


def init():
    sidebar = st.sidebar
    sidebar.markdown(get_sidebar_data())

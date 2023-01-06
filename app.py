import os.path
import pathlib

import streamlit as st

from st_pages import show_pages_from_config

hide_st_style ="""
<style>
MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""


def main():
    st.set_page_config(
        layout="wide",
        page_title="Home")

    show_pages_from_config(".streamlit/pages_sections.toml")

    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.title("Auswertung der Panoramamessung")
    st.subheader("Main Page")
    st.write("Geht es jetzt?")


if __name__ == '__main__':
    main()

import streamlit as st
from st_pages import show_pages_from_config

# hide all streamlit menus
hide_st_style ="""
<style>
MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""


def main():
    # configurate page
    st.set_page_config(
        layout="wide",  # uses the widh of the screen
        page_title="Home")  # titel of page

    # rename pages with file pages_sections.toml
    show_pages_from_config(".streamlit/pages_sections.toml")

    # Applying defined style
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # content of page
    st.title("Messauswertungen")


if __name__ == '__main__':
    main()

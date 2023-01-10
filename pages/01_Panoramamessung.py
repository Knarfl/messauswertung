import streamlit as st
import streamlit_authenticator as stauth
import time
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_option_menu import option_menu
import pandas as pd

import database as db

from functions import show_polar_chart, create_xlsx, upload_files, create_fin_dataframe
from drive import get_data

# hide all streamlit menus
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

# Applying defined style
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- USER AUTHENTICATION ---
users = db.fetch_all_users()
usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "sales_dashboard", "abcdef",
                                    cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Benutzername/Password ist falsch.")

if authentication_status is None:
    st.warning("Gib dein Benutzername und Password ein")

if authentication_status:
    st.sidebar.write(f"Herzlich Willkommen {name}")     # shows logged user
    #pwd = st.sidebar.text_input("Passwort ändern", "neues Password")

    #if st.sidebar.button('Bestätigen'):
    #    db.update_pwd(username, pwd)

    authenticator.logout("Logout", "sidebar")           # Logout Button
    # file uploader field
    uploaded_files = st.sidebar.file_uploader("Wähle Excel-Dateien aus", accept_multiple_files=True, type='xls')
    # list of drop-down-menu
    list_keys = ['Keine Datei']

    if uploaded_files is not None:
        # create menubar
        selected = option_menu(
            menu_title=None,
            options=["Daten", "Diagramme", "Export"],
            icons=["table", "bar-chart-line-fill", "download"],
            menu_icon="cast",
            default_index=0,    # selected Option of list
            orientation="horizontal"
        )

        # calculate number of uploaded files
        len_uploaded_files = len(uploaded_files)
        # shows uploaded files
        st.sidebar.write(f"Es wurden {len_uploaded_files}/24 nötigen Dateien eingelesen.")
        # warning because of too less files
        if 24 > len_uploaded_files > 0:
            st.sidebar.warning("Es wurden zu wenig Daten eingelesen")

        dict_data = upload_files(uploaded_files)    # dictionary of all files and content
        list_keys = list(dict_data.keys())          # list of all angles of files

        if len_uploaded_files > 0:
            #  select box of filter for power selection
            type_filter = st.sidebar.selectbox("Filtertyp wählen",
                                               ["TETRA Power Median Average", "TETRA Power Median Max"])

            # create formatted dataframe of alle files and content
            df_result, dict_lac = create_fin_dataframe(dict_data, type_filter, -115)
            # create a list from dataframe columns to get option for multi select field to delete columns
            options = df_result.columns.values.tolist()
            # multi select field
            option = st.sidebar.multiselect(
                'Nicht benötigte LAC entfernen',
                options)
            # create new dataframe without selected options in multiselect
            df_result = df_result.drop(option, axis=1)

            # get data from config file and create a dictionary
            dic_category = get_data("config.json")

            #def highlight_max(s):
            #    is_max = s == s.max()
            #    return ["color: #000000" if v else "" for v in is_max]

            # definition of color mapping with coloration from dictionary of config
            def color_mapping(val):
                if val >= -85:
                    color = dic_category['category']['best']['color']
                    text = "white"
                elif -88 <= val < -85:
                    color = dic_category['category']['good']['color']
                    text = "black"
                elif -90 <= val < -88:
                    color = dic_category['category']['medium']['color']
                    text = "black"
                elif -94 <= val < -90:
                    color = dic_category['category']['bad']['color']
                    text = "white"
                elif val < -94:
                    color = dic_category['category']['worst']['color']
                    text = "white"
                else:
                    color = 'black'
                    text = "white"

                return f'background-color: {color}; color: {text}'

        if selected == "Daten":     # menubar second section

            if len_uploaded_files > 0:
                # Erstelle ein Dropdown-Menü mit den Schlüsseln des Dictionarys als Optionen
                key = st.sidebar.selectbox("Wählen Sie einen Datensatz aus", list_keys)

                if key is not None:
                    # Zeige den Wert des gewählten Schlüssels im Dictionary im GUI an
                    st.write(f"Antennenausrichtung: {key}°")
                    df = pd.DataFrame.from_dict(dict_data[key])
                    filtered_df = dataframe_explorer(df)
                    st.dataframe(filtered_df, use_container_width=True)
                    #st.write(dict_data[key])

                st.dataframe(df_result.style.applymap(color_mapping))

            else:
                st.info("Es wurden keine Daten eingelesen")
                st.sidebar.write(":blue[Der Dateiname der Excel-Datei muss mit \"_Winkel\" enden. Somit wird "
                                 "sichergestellt, dass die Daten zu jeder Zeit dem jeweiligen Winkel zugeordnet "
                                 "werden können.]")
                st.sidebar.write(":blue[Beispiel: LHN-Westportal_330.xls]")

        if selected == "Diagramme":
            if len_uploaded_files > 0:
                fig_polar, fig_linear = show_polar_chart(df_result)
                st.write(fig_polar)
                st.write(fig_linear)
            else:
                st.info("Es wurden keine Daten eingelesen")

        if selected == "Export":
            if len_uploaded_files > 0:
                with st.form("my_form"):
                    col1, col2 = st.columns(2)

                    list_form = ["creator", "company", "date", "project","coordinates", "h_nn", "h_a", "gain_a", "attenuation"]
                    time_now = time.strftime("%d.%m.%Y, %H:%M")

                    with col1:
                        st.subheader("Kopf- und Fußzeile")
                        creator = st.text_input("Name des Erstellers", f"{name}")
                        company = st.text_input("Ausführende Firma", "DB Bahnbau Gruppe GmbH")
                        date = st.text_input("Datum und Uhrzeit", "25.02.2022, 14:30 Uhr bis 15:30 Uhr")
                        project = st.text_input("Projektname")
                        coordinates = st.text_input("Koordinaten")

                    with col2:
                        st.subheader("Messparameter")
                        h_nn = st.number_input("Höhe über N.N. [m]")
                        h_a = st.number_input("Antennenhöhe [m]")
                        gain_a = st.number_input("Antennengewinn [dBi]", 12.0)
                        attenuation = st.number_input("Kabeldämpfung [dB]", 2.0)

                    list_values_form = [creator, company, date, project, coordinates, h_nn, h_a, gain_a, attenuation]
                    dict_form = dict(zip(list_form, list_values_form))

                    submitted = st.form_submit_button("Bestätigen")

                if submitted:
                    with st.spinner('Die Excel-Datei wird erstellt.'):
                        wb = create_xlsx("Panoramamessung_template.xlsx", dict_form, df_result, dict_lac, 'TETRA BOS Frequenztabelle.xlsx')
                    if isinstance(wb, int):
                        st.error("Es sind mehr als 15 LAC in der Tabelle. Es können maximal 15 LAC dargestellt werden.")
                        st.info(f"Entfernen sie {wb} LAC.")
                    else:
                        st.success("Die Excel-Datei kann jetzt heruntergeladen werden.")
                        st.download_button('Download xlsx', data=wb, file_name='Panoramamessung.xlsx')
                        st.balloons()

            else:
                st.info("Es wurden keine Daten eingelesen")

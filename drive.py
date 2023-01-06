import json
import os
import streamlit as st
from deta import Deta
from dotenv import load_dotenv  # pip install python-dotenv


def init_drive(name):
    # load key from .env
    load_dotenv(".env")
    DETA_KEY = os.getenv(name)
    # open deta drive with key
    deta_drive = Deta(DETA_KEY)
    # create drive

    return deta_drive

def create_drive(deta_drive, name):
    data_drive = deta_drive.Drive(name)

    return data_drive

###################################
#name_key = "DETA_DRIVE" #local
#deta = init_drive(name_key) # local
DETA_KEY = st.secrets["DETA_DRIVE"] # deployed
deta = Deta(DETA_KEY) # deployed
##################################

name_drive = "data_pano"
data = create_drive(deta, name_drive)


def put_data_to_drive(name_data, path_data):
    data.put(name_data, path=path_data)
    return


def get_data(file_name):
    large_file = data.get(file_name)
    with open(file_name, "wb+") as f:
        for chunk in large_file.iter_chunks(4096):
            f.write(chunk)

    with open(file_name, "r") as f:
        data_json = json.load(f)
    return data_json


def get_file(filename):
    return data.get(filename)

#put_data_to_drive(data, "TETRA BOS Frequenztabelle.xlsx", "./TETRA BOS Frequenztabelle.xlsx")
#put_data_to_drive(data, "Panoramamessung_template.xlsx", "./Panoramamessung_template.xlsx")


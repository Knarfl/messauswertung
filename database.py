import os

import streamlit
import streamlit_authenticator as stauth
from deta import Deta  # pip install deta
from dotenv import load_dotenv  # pip install python-dotenv

###############################################
# Load the environment variables
#load_dotenv(".env")  # local
#DETA_KEY = os.getenv("DETA_KEY")  # deployed
DETA_KEY = streamlit.secrets["DETA_KEY"]
##############################################
# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("user_db")


def insert_user(username, name, password):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"key": username, "name": name, "password": password})


def fetch_all_users():
    """Return a dict of all users"""
    res = db.fetch()
    return res.items


def get_user(username):
    """If not found, the function will return None"""
    return db.get(username)


def update_user(username, updates):
    """If the item is updated, returns None. Otherwise, an exception is raised"""
    return db.update(updates, username)
# update_user("knarfl", updates={"name": "Neuer Name"})


def update_pwd(username, new_pwd):
    hashed_pwd = stauth.Hasher(new_pwd).generate()
    return db.update(username, {"password": hashed_pwd})


def delete_user(username):
    """Always returns None, even if the key does not exist"""
    return db.delete(username)

# delete_user("knarfl")

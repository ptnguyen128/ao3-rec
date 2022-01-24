import json
from os import path

import streamlit as st
from src import bookmarks_stats

def run():
    # vars
    oneshot_only = False
    include_kudos = False
    include_bookmarks = False

    # Main setup
    st.header("Your Bookmarks")
    st.markdown("""
        Please enter a valid AO3 username.
        Make sure your bookmarks are public.
        """)
    ## main input - username
    username = st.text_input('AO3 username', value="")
    with st.expander("Not sure if your bookmarks are public?"):
        st.write(f"""
            Click [here](https://archiveofourown.org/users/{username}/bookmarks) to see your bookmarks. \n
            Click on the `Edit` button of each one, uncheck `Private bookmark` and check the `Rec` box instead!
            """)
    filter_options = ['oneshot only']
    filters = st.multiselect("Filters", filter_options)
    if 'oneshot only' in filters:
        oneshot_only = True

    # button to navigate to bookmarks stats page
    if st.button("Click here to check your bookmarks' stats."):
        bookmarks_stats.get_bookmarks_stats(username, oneshot_only, include_kudos, include_bookmarks)

def get_username():
    return username


if __name__ == "__main__":
    run()
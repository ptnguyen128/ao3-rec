from json import JSONDecodeError

import streamlit as st
from src import bookmarks_stats
import subprocess
import sys
from os import path
import time

def get_username():
    return username

oneshot_only = False
include_kudos = False
include_bookmarks = False

# Main setup
st.title('AO3 Fanfic Recommender')
st.caption("""
This app takes in your AO3 bookmarks and recommends other fanfics that you might enjoy! (Hopefully) \n
Created by [@ausoIeil](https://twitter.com/ausoIeil). Still under development.
""")

st.header("Your Bookmarks")
st.markdown("""
    Please enter a valid AO3 username.
    Make sure your bookmarks are public.
    """)
## main input - username
username = st.text_input('AO3 username', value="")
file_path = f"data/{username}_bookmarks.txt"
if not path.exists(file_path):
    with st.spinner("Just a little bit..."):
        p = subprocess.Popen([f"{sys.executable}", "crawlers.py", f"{username}"])
        poll = p.poll()
        if poll is not None:
            st.success("Done!")
with st.expander("Not sure if your bookmarks are public?"):
    st.write(f"""
        Click [here](https://archiveofourown.org/users/{username}/bookmarks) to see your bookmarks. \n
        Click on the `Edit` button of each one, uncheck `Private bookmark` and check the `Rec` box instead!
        """)

# TODO: include these later
# filter_options = ['oneshot only', 'include_kudos', 'include_bookmarks']
filter_options = ['oneshot only']
filters = st.multiselect("Filters", filter_options)
if 'oneshot only' in filters:
    oneshot_only = True
# if 'include_kudos' in filters:
#     include_kudos = True
# if 'include_bookmarks' in filters:
#     include_bookmarks = True

# button to navigate to bookmarks stats page
with st.expander("Click here to check your bookmarks' stats."):
    try:
        bookmarks_stats.get_bookmarks_stats(username, oneshot_only, include_kudos, include_bookmarks)
    except JSONDecodeError:
        with st.spinner("Just a little bit..."):
            time.sleep(20)
            st.error("Please wait and reload the page...")

if st.button("Reload page to see your stats!"):
    st.experimental_rerun()
# number of fics to display
# number = st.slider("How many fics would you like to read?", 1, 20)

# # recommend new fics from bookmarked authors
# if st.button("Click here to check out other fics from your favorite authors."):
#     df = author_rec.get_all_fics(username, oneshot_only)
#     ranked_df = df.sort_values('score', ascending=False).head(number)
#
#     st.write("You may want to check out these fics from your favorite authors: \n")
#     for idx, row in ranked_df.iterrows():
#         st.write(f"[{row['title']}]({row['url']}) - by {row['author']} \n")

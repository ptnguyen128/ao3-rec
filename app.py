from json import JSONDecodeError

import streamlit as st
from src import bookmarks_stats
import subprocess
import sys
import time

_debug_option = False


@st.cache
def wait_a_bit(sleep_time):
    time.sleep(sleep_time)
    return sleep_time

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
with st.expander("Not sure if your bookmarks are public?"):
    st.write(f"""
        Click [here](https://archiveofourown.org/users/{username}/bookmarks) to see your bookmarks. \n
        Click on the `Edit` button of each one, uncheck `Private bookmark` and check the `Rec` box instead!
        """)

if username != '':
    subprocess.Popen([f"{sys.executable}", "crawlers.py", f"{username}"])
    # artificial wait time until subprocess finishes
    with st.spinner("Just a little bit..."):
        r = wait_a_bit(30)

    # set all filter vars to false
    oneshot_only = False
    completed_only = False
    include_kudos = False
    include_bookmarks = False

    filter_options = ['oneshot only', 'completed only']
    filters = st.multiselect("Filters", filter_options)
    if 'oneshot only' in filters:
        oneshot_only = True
    if 'completed only' in filters:
        completed_only = True
    # if 'include_kudos' in filters:
    #     include_kudos = True
    # if 'include_bookmarks' in filters:
    #     include_bookmarks = True
    with st.expander("Your bookmarks' stats."):
        try:
            bookmarks_stats.get_bookmarks_stats(username, oneshot_only, completed_only,
                                                include_kudos, include_bookmarks, debug=_debug_option)
        except JSONDecodeError:
            st.error("Please check your username again, or click this button try again in a few.")
            if st.button("Click to load your results"):
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
